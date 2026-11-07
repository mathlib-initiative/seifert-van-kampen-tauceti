#!/usr/bin/env python3
"""Export selected proof ideas and invocation ranges alongside the statement annotations.

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

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
NS = 'org.mathlib-initiative.formal-companion.overlay'
CONFIG = 'informal/proofsteps.json'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_targets(config, library):
    """Refuse stale ranges before generating or replacing any annotation."""
    if config.get('schema') != 'svk-tauceti/proof-steps' or config.get('schema_version') != 1:
        raise ValueError('unsupported proofsteps.json schema')
    if not re.fullmatch(r'[0-9a-f]{40}', config.get('library', {}).get('commit', '')):
        raise ValueError('proof steps need a pinned library commit')
    result = {}
    for step in config['steps']:
        sid = step['id']
        if not re.fullmatch(r'[1-9][0-9]*\.[1-9][0-9]*-[a-z][a-z0-9-]*', sid) or sid in result:
            raise ValueError(f'invalid or repeated proof-step id: {sid}')
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


def proof_boxes(build, config, fc, markers):
    aux = fc.read_aux(build.aux)
    raw = build.aux.read_text()
    actual = []
    for match in re.finditer(r'\\svk@auxstep(?![A-Za-z@])', raw):
        groups = fc._groups(raw, match.end(), 2)
        if groups is None:
            raise ValueError('malformed proof-idea marker')
        actual.append(tuple(groups[0]))
    expected = [(s['id'], s['title']) for s in config['steps']]
    if actual != expected:
        raise ValueError('proof-idea markers do not match proofsteps.json in order and title')
    geo = markers.Geometry(aux.geometry, fc.pdf_pages(build.pdf))
    params = markers.Params.of(build.config.boxes)
    ink = markers.render_pages(build.pdf, geo, params)
    rows = []
    for step in config['steps']:
        name = 'fc:proof:' + step['id']
        start = aux.positions[name + ':start']
        above = aux.positions[name + ':above']
        end = aux.positions.get(name + ':below', aux.positions[name + ':end'])
        finish = markers.effective_end(geo, start, end, None)
        upper = geo.from_top(above) if above['abspage'] == start['abspage'] else None
        spans = markers.region_spans(geo, ink, params, start, upper, finish, None, step['id'])
        rows.append({'id': step['id'], 'title': step['title'],
                     'boxes': markers.to_fractions(geo, [s.box() for s in spans])})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--formal-companion', required=True, type=Path)
    parser.add_argument('--library-src', required=True, type=Path)
    parser.add_argument('--packages-src', type=Path)
    parser.add_argument('--build-dir', required=True, type=Path)
    parser.add_argument('--pdf-url', required=True)
    args = parser.parse_args()
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
    def runner(argv):
        return subprocess.run([sys.executable, str(args.formal_companion / 'scripts/cf.py'), *argv],
                              text=True, capture_output=True)
    base_export.export(ROOT, convention='informal-markers', commit=head, extra=extra, runner=runner)
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
                    'title': 'Proof idea: ' + step['title'],
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
                    'confirmed_by_human': False}, 'locator': {'physical': [b[0] for b in region['boxes']],
                                                            'printed': [b[0] for b in region['boxes']]}}}}
            (directory / f'proof-{step["id"]}-{n:02d}.json').write_bytes(defaults.dumps(record))
    found = sync.read_annotations(ROOT)
    if found.problems:
        raise ValueError('; '.join(found.problems))
    manifest['count'] = sync.annotation_count(found.files)
    manifest['manifest_sha256'] = sync.manifest_sha256(found.files)
    for rel in [CONFIG, 'informal/proofsteps.sty', 'tools/proof_steps.py']:
        manifest['inputs'].append({'path': rel, 'sha256': digest((ROOT / rel).read_bytes())})
    sync.record_annotations(ROOT, manifest)
    sync.sync(ROOT)
    cache = ROOT / '.lake/overlay-pdf'
    cache.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(build.pdf, cache / 'svk-tauceti.pdf')
    report = {'pdf_sha256': digest(build.pdf.read_bytes()), 'library': config['library'],
              'proof_ideas': len(boxes), 'lean_ranges': sum(map(len, targets.values())),
              'annotations': manifest['count'], 'steps': boxes, 'confirmed_by_human': False}
    (args.build_dir / 'proof-steps-report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='steps'}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        raise SystemExit(str(error)) from error
