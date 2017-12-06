import unittest

from rms import metadata

class TestMetadata(unittest.TestCase):

    def test_guess_pack(self):
        self.assertEqual(metadata._guess_pack('WiC_Dry_Arabia'), ['WiC'])
        self.assertEqual(metadata._guess_pack('nC@Decentring'), ['nC'])
        self.assertEqual(metadata._guess_pack('WiC_nC@Decentring'), ['WiC', 'nC'])
        self.assertEqual(metadata._guess_pack('test@Dry_Arabia'), ['test'])
        self.assertEqual(metadata._guess_pack('WSVG_WiC_nC@Decentring'), ['WSVG', 'WiC', 'nC'])

    def test_extract(self):
        self.assertEqual(metadata.extract('tests/data/SY_Dry_Arabia.rms'), {
            'path': 'tests/data/SY_Dry_Arabia.rms',
            'filename': 'SY_Dry_Arabia.rms',
            'map': 'SY_Dry_Arabia',
            'megarandom': False,
            'multiple': False,
            'pack': ['SY']
        })
