"""Search through files with the given expression."""


from __future__ import print_function
from multiprocessing import Pool
import os
import signal
import sys

from redbaron import RedBaron
from redbaron.base_nodes import NodeList

from baroness.utils import (
    filenames, format_node, _load_and_save, _cache_filename, LOGGER
)


try:
    import ujson as json
except ImportError:
    import json


def search(
    files, pattern, no_cache=False, parents=0, no_color=False,
    no_linenos=False, verbose=0, processes=2
):
    """Search all files with the redbaron expression in pattern."""
    options = dict(locals())
    options.pop('files')

    LOGGER.debug('DEBUG Using options: %s', options)
    LOGGER.debug('DEBUG Using %s processes', processes)
    pool = Pool(processes, _init_worker)
    tasks = ((filename, pattern, options) for filename in filenames(files))
    try:
        for result in pool.imap_unordered(_safe_search_file, tasks):
            if not result:
                continue
            filename, output = result
            LOGGER.debug('DEBUG Searching: %s', filename)
            if output:
                LOGGER.info(output)
    except KeyboardInterrupt:
        LOGGER.critical('KeyboardInterrupt, quitting')
        sys.exit(1)
    finally:
        pool.terminate()
        pool.join()


def _init_worker():
    """Ensure that KeyboardInterrupt is ignored."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def _safe_search_file(args):
    """A wrapper for multiprocessing around _search_file."""
    try:
        return _search_file(*args)
    except Exception:
        LOGGER.exception('Error processing file')


def _search_file(filename, pattern, options):
        """Search a given filename."""
        local = locals()
        exec('def _search(root):\n    return {}'.format(pattern), globals(), local)
        _search = local['_search']

        cache_file = _cache_filename(filename)
        if not options['no_cache'] and os.path.exists(cache_file):
            with open(cache_file) as f:
                root = RedBaron(NodeList.from_fst(json.load(f)))
            for node in root:
                node.parent = root
            root.node_list.parent = root
        else:
            root = _load_and_save(filename, cache_file, no_cache=options['no_cache'])

        results = _search(root)
        output = []
        seen = set()
        if results:
            output.append(filename)
            for result in results:
                # Get the correct number of parents
                for _ in range(options['parents']):
                    result = result.parent if result.parent else result

                # Ensure that we don't print the same code twice
                if result in seen:
                    continue
                else:
                    seen.add(result)

                # format the output
                output.append(format_node(
                    result,
                    no_color=options['no_color'],
                    no_linenos=options['no_linenos']
                ))
                output.append(u'--')
            output.append(u'')
        return (filename, u'\n'.join(output))
