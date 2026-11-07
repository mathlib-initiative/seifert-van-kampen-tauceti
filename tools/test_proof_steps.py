import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('proof_steps', Path(__file__).with_name('proof_steps.py'))
proof_steps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proof_steps)


class RangeValidation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'TauCeti/Example.lean'
        self.source.parent.mkdir()
        self.source.write_text('theorem sample : True := by\n  trivial\n')
        self.config = {'schema':'svk-tauceti/proof-steps', 'schema_version':2,
            'library': {'commit':'a'*40}, 'steps':[{'id':'1.1-test', 'span':'inline', 'targets':[
                {'module':'TauCeti.Example', 'lines':[2,2],
                 'sha256':hashlib.sha256(b'  trivial\n').hexdigest(), 'role':'key'}]}]}

    def check(self):
        return proof_steps.read_targets(self.config, self.root)

    def test_valid_range_preserves_indentation(self):
        self.assertEqual(self.check()['1.1-test'][0][1], '  trivial')

    def test_source_edit_is_rejected(self):
        self.source.write_text('theorem sample : True := by\n  exact True.intro\n')
        with self.assertRaisesRegex(ValueError, 'range changed'):
            self.check()

    def test_out_of_file_range_is_rejected(self):
        self.config['steps'][0]['targets'][0]['lines']=[2,3]
        with self.assertRaisesRegex(ValueError, 'invalid Lean range'):
            self.check()

    def test_reversed_range_is_rejected(self):
        self.config['steps'][0]['targets'][0]['lines']=[2,1]
        with self.assertRaisesRegex(ValueError, 'invalid Lean range'):
            self.check()

    def test_duplicate_id_is_rejected(self):
        self.config['steps'].append(copy.deepcopy(self.config['steps'][0]))
        with self.assertRaisesRegex(ValueError, 'repeated'):
            self.check()

    def test_moving_branch_is_rejected(self):
        self.config['library']['commit']='main'
        with self.assertRaisesRegex(ValueError, 'pinned'):
            self.check()

    def test_module_cannot_escape_source_tree(self):
        self.config['steps'][0]['targets'][0]['module']='TauCeti...Example'
        with self.assertRaisesRegex(ValueError, 'invalid module'):
            self.check()

    def test_empty_targets_are_rejected(self):
        self.config['steps'][0]['targets']=[]
        with self.assertRaisesRegex(ValueError, 'no Lean target'):
            self.check()

    def test_unknown_role_is_rejected(self):
        self.config['steps'][0]['targets'][0]['role']='proof'
        with self.assertRaisesRegex(ValueError, 'target role'):
            self.check()

    def test_whole_proof_region_is_rejected(self):
        self.config['steps'][0]['span']='proof'
        with self.assertRaisesRegex(ValueError, 'sentence or equation'):
            self.check()

    def test_different_targets_must_be_separate_steps(self):
        step=self.config['steps'][0]
        step['targets'].append(copy.deepcopy(step['targets'][0]))
        with self.assertRaisesRegex(ValueError, 'split steps'):
            self.check()


class EquationGeometry(unittest.TestCase):
    class Page:
        def from_top(self, pos):
            return 800-pos['posy']/100

    def test_equation_uses_its_width_and_full_height(self):
        start={'abspage':2, 'posx':20000, 'posy':50000}
        end={'abspage':2, 'posx':38000, 'posy':50000}
        self.assertEqual(proof_steps.equation_box(self.Page(),start,end,[18000,2000,1500],2,100),
                         [2,198,278,184,39])

    def test_misaligned_equation_markers_are_rejected(self):
        start={'abspage':2, 'posx':20000, 'posy':50000}
        end={'abspage':3, 'posx':38000, 'posy':50000}
        with self.assertRaisesRegex(ValueError, 'baseline and page'):
            proof_steps.equation_box(self.Page(),start,end,[18000,2000,1500],2,100)


class ExportIntegrity(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root/'informal').mkdir()
        (self.root/'pdf-overlay').mkdir()
        for rel in ['informal/proofsteps.json', 'pdf-overlay/annotations.bundle.json']:
            (self.root/rel).write_bytes((proof_steps.ROOT/rel).read_bytes())

    def test_exported_ranges_match_the_curation(self):
        proof_steps.check_export(self.root)

    def alter(self, what):
        p=self.root/'pdf-overlay/annotations.bundle.json'
        v=json.loads(p.read_text())
        row=next(r['annotation'] for r in v['annotations'] if r['annotation'].get('kind')=='proof_step')
        ext=row['object'][0]['extensions'][proof_steps.NS]
        what(ext)
        p.write_text(json.dumps(v))

    def test_edited_snippet_is_rejected(self):
        self.alter(lambda ext: ext['snippet'].update(text='  sorry'))
        with self.assertRaisesRegex(ValueError, 'snippet differs'):
            proof_steps.check_export(self.root)

    def test_wrong_destination_is_rejected(self):
        self.alter(lambda ext: ext['destination'].update(href='https://example.org/wrong'))
        with self.assertRaisesRegex(ValueError, 'destination'):
            proof_steps.check_export(self.root)


if __name__ == '__main__':
    unittest.main()
