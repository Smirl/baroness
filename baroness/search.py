"""Search through files with the given expression."""


from __future__ import print_function
import os

from redbaron import RedBaron
from redbaron.base_nodes import NodeList

from baroness.utils import filenames


try:
    import ujson as json
except ImportError:
    import json


def search(pattern, files, no_cache, parents):
    """Search all files with the redbaron expression in pattern."""
    _search = None  # for linters
    code = 'def _search(root):\n    return {}'.format(pattern)
    print(code)
    exec code

    for filename in filenames(files):
        cache_file = os.path.join('.baroness', filename) + '.json'
        if not no_cache and os.path.exists(cache_file):
            with open(cache_file) as f:
                root = RedBaron(NodeList.from_fst(json.load(f)))
        else:
            with open(filename) as py:
                root = RedBaron(py.read())

        results = _search(root)
        if results:
            print(filename)
            for result in results:
                for _ in range(parents):
                    result = result.parent if result.parent else result
                print(result)
