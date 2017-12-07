"""Search through files with the given expression."""


from __future__ import print_function
import os

from redbaron import RedBaron
from redbaron.base_nodes import NodeList

from baroness.utils import filenames, format_node, _load_and_save, _cache_filename


try:
    import ujson as json
except ImportError:
    import json


def search(pattern, files, no_cache, parents, no_color, no_linenos):
    """Search all files with the redbaron expression in pattern."""
    local = locals()
    exec('def _search(root):\n    return {}'.format(pattern), globals(), local)
    _search = local['_search']

    for filename in filenames(files):
        cache_file = _cache_filename(filename)
        if not no_cache and os.path.exists(cache_file):
            with open(cache_file) as f:
                root = RedBaron(NodeList.from_fst(json.load(f)))
            for node in root:
                node.parent = root
            root.node_list.parent = root
        else:
            root = _load_and_save(filename, cache_file, no_cache=no_cache)

        results = _search(root)
        if results:
            print(filename)
            for result in results:
                for _ in range(parents):
                    result = result.parent if result.parent else result
                print(format_node(result, no_color=no_color, no_linenos=no_linenos))
                print('--')
            print()
