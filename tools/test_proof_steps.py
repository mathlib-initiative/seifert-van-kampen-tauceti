import copy
import hashlib
import importlib.util
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
        self.config = {'schema':'svk-tauceti/proof-steps', 'schema_version':1,
            'library': {'commit':'a'*40}, 'steps':[{'id':'1.1-test', 'targets':[
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


if __name__ == '__main__':
    unittest.main()
