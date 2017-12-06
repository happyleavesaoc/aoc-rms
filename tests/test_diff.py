import unittest

from rms import diff


class TestDiff(unittest.TestCase):

    def test_similarity(self):
        self.assertTrue(diff.similarity('tests/data/WiC_Dry_Arabia.rms', 'tests/data/WSVG_Dry Arabia.rms') > 0.9)
        self.assertTrue(diff.similarity('tests/data/SY_Dry_Arabia.rms', 'tests/data/WiC_Duopoly_v2.rms') < 0.3)

    def test_diff(self):
        lines = diff.diff('tests/data/WiC_Dry_Arabia.rms', 'tests/data/WSVG_Dry Arabia.rms')
        self.assertEqual(len(lines), 11)
