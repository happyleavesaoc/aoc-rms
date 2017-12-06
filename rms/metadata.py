"""Extract metadata from RMS file."""
import os
import re


def _guess_pack(map_name):
    """Guess the map pack name.

    WiC_nC@<map name>

    """
    if not map_name:
        return []
    candidate = re.split('_|@', map_name)[0]
    if candidate == map_name:
        return []
    if map_name[len(candidate)] == '_':
        if len(candidate) > 5:
            return []
        uppers = [l for l in candidate[1:] if l.isupper()]
        if not uppers:
            return []
    map_name = map_name[len(candidate) + 1:]
    return [candidate] + _guess_pack(map_name)


def _as_string(path):
    """Return map data as a string."""
    with open(path, 'r', encoding='latin1') as handle:
        return handle.read()


def extract(path):
    """Extract metadata from RMS file."""
    filename = os.path.basename(path)
    map_name = os.path.splitext(filename)[0]
    data = _as_string(path)
    return {
        'path': path,
        'filename': filename,
        'map': map_name,
        'pack': _guess_pack(map_name),
        'multiple': data.count('LAND_GENERATION') > 3,
        'megarandom': data.find('MEGARANDOM') > -1
    }


if __name__ == '__main__':
    import sys
    print(extract(sys.argv[1]))
