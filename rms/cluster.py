"""Cluster RMS files based on similarity."""
import glob
import os
from collections import defaultdict
from difflib import SequenceMatcher

from sklearn.cluster import DBSCAN

import rms.diff as diff


def _similarity_matrix(path):
    """Produce a dense similarity matrix for all maps in a directory."""
    files = glob.glob(os.path.join(path, '**/*.rms'), recursive=True)
    cache = defaultdict(dict)
    matrix = []
    for file_1 in files:
        row = []
        for file_2 in files:
            if file_1 == file_2:
                row.append(0)
            elif file_1 in cache and file_2 in cache[file_1]:
                row.append(cache[file_1][file_2])
            else:
                inverse_sim = 1 - diff.similarity(file_1, file_2)
                cache[file_2][file_1] = inverse_sim
                row.append(inverse_sim)
        matrix.append(row)
    return files, matrix


def _name_cluster(maps):
    """Name a cluster based on longest common substring."""
    if not maps:
        raise ValueError('at least one map required')
    answer = maps[0]
    for path in maps:
        matcher = SequenceMatcher(None, path.replace(' ', '_'), answer.replace(' ', '_'))
        match = matcher.find_longest_match(0, len(path), 0, len(answer))
        answer = path[match.a:match.a + match.size]
    return os.path.splitext(os.path.basename(answer))[0].replace('_', ' ').strip()


def cluster(path, similarity, min_size):
    """Return clusters for maps in a directory."""
    if similarity < 0 or similarity > 1:
        raise ValueError('similarity out of bounds (0.0-1.0)')
    if min_size < 1:
        raise ValueError('minimum size out of bounds (> 0)')
    labels, data = _similarity_matrix(path)
    eps = 1 - similarity
    results = DBSCAN(eps=eps, min_samples=1, metric='precomputed').fit_predict(data)
    clusters = defaultdict(list)
    for label_index, cluster_number in enumerate(results):
        clusters[cluster_number].append(labels[label_index])
    return [cluster for cluster in clusters.values() if len(cluster) >= min_size]


if __name__ == '__main__':
    import sys
    for m in cluster(sys.argv[1], 0.7, 1):
        print(_name_cluster(m), ' -> ', m)
