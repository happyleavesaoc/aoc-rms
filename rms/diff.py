"""Compare RMS files."""
import difflib

_CACHE = {}


def normalize(path):
    """Read file and remove various non-essential data to make it easier to diff.

    - comments
    - whitespace
    """
    if path in _CACHE:
        return _CACHE[path]
    lines = []
    with open(path, 'r', encoding='latin1') as handle:
        for line in handle.readlines():
            pos = line.find('/*')
            if pos > -1:
                line = line[:pos]
            line = ' '.join(line.split()).strip()
            if line:
                lines.append(line)
    _CACHE[path] = lines
    return lines


def get_lines(rms_1, rms_2):
    """Get normalized lines from both files."""
    return normalize(rms_1), normalize(rms_2)


def similarity(rms_1, rms_2):
    """Compute similarity between two RMS files."""
    return difflib.SequenceMatcher(None, *get_lines(rms_1, rms_2)).ratio()


def diff(rms_1, rms_2):
    """Get diff between two RMS files."""
    return list(difflib.unified_diff(*get_lines(rms_1, rms_2)))


if __name__ == '__main__':
    import sys
    for l in diff(sys.argv[1], sys.argv[2]):
        print(l)
    print(similarity(sys.argv[1], sys.argv[2]))
