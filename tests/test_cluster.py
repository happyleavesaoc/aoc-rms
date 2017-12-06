import unittest

from rms import cluster


class TestDiff(unittest.TestCase):

    def test_similarity_matrix(self):
        labels, matrix = cluster._similarity_matrix('tests/data')
        self.assertEqual(len(labels), len(matrix))
        for row in matrix:
            self.assertEqual(len(matrix), len(row))
            for value in row:
                self.assertTrue(value >= 0.0 and value <= 1.0)

    def test_name_cluster_multiple(self):
        name = cluster._name_cluster(['tests/data/SY_Dry_Arabia.rms', 'tests/data/WSVG_Dry Arabia.rms'])
        self.assertEqual(name, 'Dry Arabia')

    def test_name_cluster_single(self):
        name = cluster._name_cluster(['tests/data/SY_Dry_Arabia.rms'])
        self.assertEqual(name, 'SY Dry Arabia')

    def test_cluster(self):
        clusters = cluster.cluster('tests/data', 0.7, 1)
        self.assertEqual(len(clusters), 2)

    def test_lax_cluster(self):
        clusters = cluster.cluster('tests/data', 0.1, 1)
        self.assertEqual(len(clusters), 1)

    def test_only_duplicate_cluster(self):
        clusters = cluster.cluster('tests/data', 0.7, 2)
        self.assertEqual(len(clusters), 1)
