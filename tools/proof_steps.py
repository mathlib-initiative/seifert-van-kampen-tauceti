#!/usr/bin/env python3
"""Export individual proof sentences/equations and their exact Lean ranges alongside the statement annotations.

Project adapter for this exposition, using the existing PDF-marker geometry and
Literature Links format. It does not modify TauCeti or the generated runtimes.
Run from the repository root after building the canonical PDF and committing
informal/markers.json. See README.md for the complete sequence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
NS = 'org.mathlib-initiative.formal-companion.overlay'
CONFIG = 'informal/proofsteps.json'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_targets(config, library):
    """Refuse stale ranges before generating or replacing any annotation."""
    if config.get('schema') != 'svk-tauceti/proof-steps' or config.get('schema_version') != 2:
        raise ValueError('unsupported proofsteps.json schema')
    if not re.fullmatch(r'[0-9a-f]{40}', config.get('library', {}).get('commit', '')):
        raise ValueError('proof steps need a pinned library commit')
    result = {}
    for step in config['steps']:
        sid = step['id']
        if not re.fullmatch(r'[1-9][0-9]*\.[1-9][0-9]*-[a-z][a-z0-9-]*', sid) or sid in result:
            raise ValueError(f'invalid or repeated proof-step id: {sid}')
        if step.get('span') not in ('inline', 'display'):
            raise ValueError(f'{sid}: proof step must mark a sentence or equation')
        if len(step['targets']) > 1:
            raise ValueError(f'{sid}: split steps with different Lean targets')
        if not step['targets']:
            raise ValueError(f'{sid}: no Lean target')
        targets = []
        for target in step['targets']:
            module = target['module']
            if not re.fullmatch(r'TauCeti(?:\.[A-Za-z_][A-Za-z0-9_]*)+', module):
                raise ValueError(f'{sid}: invalid module')
            bounds = target['lines']
            raw = (library / (module.replace('.', '/') + '.lean')).read_bytes().splitlines(keepends=True)
            if len(bounds) != 2 or any(type(n) is not int for n in bounds) or not 1 <= bounds[0] <= bounds[1] <= len(raw):
                raise ValueError(f'{sid}: invalid Lean range')
            code = b''.join(raw[bounds[0] - 1:bounds[1]])
            if digest(code) != target['sha256']:
                raise ValueError(f'{sid}: Lean range changed in {module}:{bounds}')
            if target['role'] not in ('key', 'support'):
                raise ValueError(f'{sid}: unsupported target role')
            targets.append((target, code.decode('utf-8').rstrip('\n')))
        result[sid] = targets
    return result


def equation_box(geo, start, end, dimensions, pad, sp_per_bp):
    """Bound just the measured math box, never the surrounding paragraph."""
    width, height, depth = [int(n) / sp_per_bp for n in dimensions]
    if start['abspage'] != end['abspage'] or abs(start['posy'] - end['posy']) > 2:
        raise ValueError('equation markers must share one baseline and page')
    left = start['posx'] / sp_per_bp
    if abs((end['posx'] - start['posx']) / sp_per_bp - width) > .02:
        raise ValueError('equation width differs from its measured math box')
    baseline = geo.from_top(start)
    return [start['abspage'], left-pad, baseline-height-pad,
            width+2*pad, height+depth+2*pad]


def proof_boxes(build, config, fc, markers):
    aux = fc.read_aux(build.aux)
    raw = build.aux.read_text()
    actual, dimensions = [], {}
    for command, count in [('step', 3), ('math', 4)]:
        for match in re.finditer(r'\\svk@aux'+command+r'(?![A-Za-z@])', raw):
            groups = fc._groups(raw, match.end(), count)
            if groups is None:
                raise ValueError('malformed proof-step marker')
            values = groups[0]
            if command == 'step':
                actual.append(tuple(values))
            else:
                if values[0] in dimensions:
                    raise ValueError('duplicate equation dimensions')
                dimensions[values[0]] = values[1:]
    expected = [(s['id'], s['span'], s['title']) for s in config['steps']]
    if actual != expected:
        raise ValueError('sentence/equation markers do not match proofsteps.json in order and title')
    if set(dimensions) != {s['id'] for s in config['steps'] if s['span']=='display'}:
        raise ValueError('equation dimensions do not match the marked equations')
    geo = markers.Geometry(aux.geometry, fc.pdf_pages(build.pdf))
    params = markers.Params.of(build.config.boxes)
    ink = markers.render_pages(build.pdf, geo, params)
    rows = []
    for step in config['steps']:
        name = 'fc:proof:' + step['id']
        start, end = aux.positions[name + ':start'], aux.positions[name + ':end']
        if step['span'] == 'inline':
            spans = markers.notion_spans(geo, ink, params, start, end, step['id'])
            boxes = [s.box() for s in spans]
        else:
            boxes = [equation_box(geo, start, end, dimensions[step['id']], params.pad_bp, fc.SP_PER_BP)]
        rows.append({'id': step['id'], 'title': step['title'], 'span': step['span'],
                     'boxes': markers.to_fractions(geo, boxes)})
    return rows



def check_export(root=ROOT):
    config = json.loads((root / CONFIG).read_text())
    bundle = json.loads((root / 'pdf-overlay/annotations.bundle.json').read_text())
    rows = [r['annotation'] for r in bundle['annotations'] if r['annotation'].get('kind') == 'proof_step']
    expected = {}
    for step in config['steps']:
        for n, target in enumerate(step['targets'], 1):
            expected[(f'proof-{step["id"]}', f'proof-{step["id"]}-{n}')] = target
    seen = set()
    for row in rows:
        for end in row['object']:
            ext = end['extensions'][NS]
            key = (row['id'], ext['declaration']['id'])
            if key not in expected or key in seen:
                raise ValueError(f'unexpected or repeated proof-step target: {key}')
            seen.add(key)
            target = expected[key]
            location = {'module': target['module'], 'lines': target['lines']}
            if target.get('declaration'):
                location['declaration'] = target['declaration']
            if end['location'] != location or end['version'] != config['library']['commit'] or end['uri'] != config['library']['url']:
                raise ValueError(f'{key}: wrong Lean source location')
            code = ext['snippet']['text']
            if digest((code+'\n').encode()) != target['sha256'] or ext['snippet']['line'] != target['lines'][0]:
                raise ValueError(f'{key}: exported snippet differs from the pinned range')
            first, last = target['lines']
            href = config['library']['url']+'/blob/'+config['library']['commit']+'/'+target['module'].replace('.', '/')+'.lean'
            if ext['destination']['href'] != href or ext['destination']['fragment'] != f'L{first}-L{last}':
                raise ValueError(f'{key}: destination does not select the full range')
            if row['relation'] != ('relatedMatch' if target['role']=='support' else 'closeMatch'):
                raise ValueError(f'{key}: wrong proof-step relation')
            for subject in row['subject']:
                rect = subject['location']['rect']
                if len(rect)!=4 or any(x < 0 for x in rect) or rect[2] <= 0 or rect[3] <= 0 or rect[0]+rect[2]>1 or rect[1]+rect[3]>1:
                    raise ValueError(f'{key}: invalid PDF box')
    if seen != set(expected):
        raise ValueError('missing proof-step targets')
    print(f'PASS {len(config["steps"])} sentence/equation steps, {len(seen)} pinned Lean ranges')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='check exported snippets and ranges offline')
    parser.add_argument('--formal-companion', type=Path)
    parser.add_argument('--library-src', type=Path)
    parser.add_argument('--packages-src', type=Path)
    parser.add_argument('--build-dir', type=Path)
    parser.add_argument('--pdf-url')
    args = parser.parse_args()
    if args.check:
        check_export()
        return
    if not all([args.formal_companion, args.library_src, args.build_dir, args.pdf_url]):
        parser.error('export requires --formal-companion, --library-src, --build-dir and --pdf-url')
    config = json.loads((ROOT / CONFIG).read_text())
    targets = read_targets(config, args.library_src)
    informal = json.loads((ROOT / 'informal/informalize.json').read_text())
    if config['library']['commit'] != informal['library']['commit']:
        raise ValueError('proof-step library differs from the exposition')
    # Both imports are the already vendored runtime; nothing is written into it.
    sys.path.insert(0, str(ROOT / 'informal/tools'))
    import fccommon as fc
    import extract_markers as markers
    build = fc.Build(args.build_dir)
    for path in (ROOT / 'informal').rglob('*'):
        if path.is_file() and path.name != 'markers.json':
            built = build.src / path.relative_to(ROOT / 'informal')
            if not built.is_file() or built.read_bytes() != path.read_bytes():
                raise ValueError(f'PDF was not built from current {path.relative_to(ROOT)}')
    boxes = proof_boxes(build, config, fc, markers)
    sys.path.insert(0, str(args.formal_companion / 'scripts'))
    from overlay import export as base_export, sync, defaults
    head = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
    extra = ['--pdf', str(build.pdf), '--pdf-url', args.pdf_url,
             '--library-src', str(args.library_src), '--source-title', json.loads((ROOT / 'pdf-overlay/overlay.config.json').read_text())['title']]
    if args.packages_src:
        extra += ['--packages-src', str(args.packages_src)]
    # Export the committed source from a clean snapshot: the previous generated
    # annotations in ROOT may legitimately be dirty while regenerating them.
    with tempfile.TemporaryDirectory(prefix='svk-proof-export-') as tmp:
        snapshot = Path(tmp) / 'source'
        subprocess.run(['git', '-C', str(ROOT), 'worktree', 'add', '--detach', str(snapshot), head],
                       check=True, capture_output=True)
        try:
            def runner(argv):
                argv = list(argv)
                argv[2] = str(snapshot)
                return subprocess.run([sys.executable, str(args.formal_companion / 'scripts/cf.py'), *argv],
                                      text=True, capture_output=True)
            base_export.export(ROOT, convention='informal-markers', commit=head, extra=extra, runner=runner)
        finally:
            subprocess.run(['git', '-C', str(ROOT), 'worktree', 'remove', str(snapshot)],
                           check=True, capture_output=True)
    manifest = json.loads((ROOT / 'pdf-overlay/GENERATED.json').read_text())['annotations']
    # Preserve the existing statement records; place steps beside an unambiguous owner.
    owner_kinds = {'4.1':'theorem', '4.2':'definition', '5.1':'theorem',
                   '6.1':'definition', '6.3':'proposition', '6.4':'theorem'}
    for item, kind in owner_kinds.items():
        section = item.split('.')[0]
        aid = kind + '-' + item
        directory = ROOT / 'annotations' / section / aid
        directory.mkdir(exist_ok=True)
        for path in list((ROOT / 'annotations' / section).glob('*.json')):
            if json.loads(path.read_text()).get('id') == aid:
                path.replace(directory / path.name)
    for step, region in zip(config['steps'], boxes):
        section = step['item'].split('.')[0]
        kind = owner_kinds.get(step['item'])
        dirname = kind + '-' + step['item'] if kind else 'proof-' + step['id']
        directory = ROOT / 'annotations' / section / dirname
        directory.mkdir(exist_ok=True)
        for n, (target, code) in enumerate(targets[step['id']], 1):
            iid = 'proof-' + step['id']
            subjects = []
            for page, x, y, w, h in region['boxes']:
                subjects.append({'location': {'page': page, 'rect': [x,y,w,h]},
                    'title': step['title'],
                    'extensions': {NS: {'region': f'{iid}@p{page:03d}'}}})
            loc = {'module': target['module'], 'lines': target['lines']}
            if target.get('declaration'):
                loc['declaration'] = target['declaration']
            start, end = target['lines']
            obj = {'location': loc, 'title': target['title'], 'role': target['role'],
                'extensions': {NS: {
                    'declaration': {'id': f'{iid}-{n}', 'kind': 'proof_step'},
                    'destination': {'href': config['library']['url'] + '/blob/' + config['library']['commit'] + '/' + target['module'].replace('.', '/') + '.lean',
                                    'fragment': f'L{start}-L{end}', 'resolution': 'exact'},
                    'snippet': {'line': start, 'text': code}}}}
            record = {'id': iid, 'kind': 'proof_step',
                'relation': 'relatedMatch' if target['role'] == 'support' else 'closeMatch',
                'note': target['title'], 'subject': subjects, 'object': [obj],
                'extensions': {NS: {'provenance': {'actor': 'agent', 'method': 'agent_annotation',
                    'confirmed_by_human': False}, 'locator': {'physical': sorted({b[0] for b in region['boxes']}),
                                                            'printed': sorted({b[0] for b in region['boxes']})}}}}
            (directory / f'proof-{step["id"]}-{n:02d}.json').write_bytes(defaults.dumps(record))
    found = sync.read_annotations(ROOT)
    if found.problems:
        raise ValueError('; '.join(found.problems))
    manifest['count'] = sync.annotation_count(found.files)
    manifest['manifest_sha256'] = sync.manifest_sha256(found.files)
    inputs = {row['path']: row for row in manifest['inputs']}
    source_paths = list((ROOT / 'informal').rglob('*.tex')) + list((ROOT / 'informal').glob('*.sty'))
    for rel in [CONFIG, 'tools/proof_steps.py', *[p.relative_to(ROOT).as_posix() for p in source_paths]]:
        inputs[rel] = {'path': rel, 'sha256': digest((ROOT / rel).read_bytes())}
    manifest['inputs'] = [inputs[k] for k in sorted(inputs)]
    sync.record_annotations(ROOT, manifest)
    sync.sync(ROOT)
    cache = ROOT / '.lake/overlay-pdf'
    cache.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(build.pdf, cache / 'svk-tauceti.pdf')
    report = {'pdf_sha256': digest(build.pdf.read_bytes()), 'library': config['library'],
              'proof_steps': len(boxes), 'lean_ranges': sum(map(len, targets.values())),
              'annotations': manifest['count'], 'steps': boxes, 'confirmed_by_human': False}
    (args.build_dir / 'proof-steps-report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='steps'}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        raise SystemExit(str(error)) from error
