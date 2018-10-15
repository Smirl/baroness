"""Utils shared by commands."""

from argparse import _SubParsersAction
from glob import glob
from itertools import repeat, count
import logging
import os
import sys

from builtins import str
from distutils.dir_util import mkpath
from redbaron import RedBaron
from redbaron.syntax_highlight import python_highlight

try:
    import ujson as json
except ImportError:
    import json


LOGGER = logging.getLogger('baroness')
LOGGER.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
LOGGER.addHandler(ch)


def filenames(files):
    """
    Yield string filenames given filenames or globs, else walk current dir.

    Input can either be an empty list, meaning we walk the current directory
    and yield python files. Or can be a list of filenames and/or glob patterns
    which we expand, and filter for python files.
    """
    LOGGER.debug('Expanding globs: %s', files)
    directories = []
    if files:
        for pattern in files:
            for filename in glob(pattern):
                if os.path.isdir(filename):
                    directories.append(filename)
                elif os.path.splitext(filename)[1] == '.py':
                    yield os.path.relpath(filename)

    if not (files or directories):
        directories.append('.')

    LOGGER.debug('Searching for python files in: %s', directories)
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if os.path.splitext(filename)[1] == '.py':
                    yield os.path.relpath(os.path.join(root, filename))


def set_default_subparser(self, name, args=None):
    """Set the default subparser on an ArgParser."""
    subparser_found = False
    for arg in sys.argv[1:]:
        if arg in ['-h', '--help']:  # global help if no subparser
            break
    else:
        for x in self._subparsers._actions:
            if not isinstance(x, _SubParsersAction):
                continue
            for sp_name in x._name_parser_map.keys():
                if sp_name in sys.argv[1:]:
                    subparser_found = True
        if not subparser_found:
            # insert default in first position, this implies no
            # global options without a sub_parsers specified
            if args is None:
                sys.argv.insert(1, name)
            else:
                args.insert(0, name)


def format_node(node, no_color=False, no_linenos=False):
    """Add line numbers to the str of a node."""
    if sys.stdin.isatty and not no_color:
        lines = list(map(
            lambda x: str(x, 'utf-8'),
            python_highlight(node.dumps()).splitlines()
        ))

        def format_lineno(lineno):
            return str(python_highlight(str(lineno)), 'utf-8')
    else:
        lines = node.dumps().splitlines()

        def format_lineno(lineno):
            return str(lineno)

    if not no_linenos:
        try:
            linenos = count(node.absolute_bounding_box.top_left.line)
        except AttributeError:
            linenos = repeat(u'**')
        except ValueError:
            linenos = count()
        lines = [
            u'{}-{}'.format(format_lineno(lineno).strip(), line)
            for lineno, line in zip(linenos, lines)
        ]

    return u'\n'.join(lines)


def _load_and_save(filename, cache_file, no_cache=False):
    """Save a tree to file and return the parsed RedBaron."""
    mkpath(os.path.split(cache_file)[0])

    with open(filename) as py:
        root = RedBaron(py.read())
        if not no_cache:
            with open(cache_file, 'w') as output:
                json.dump(root.fst(), output)

    return root


def _cache_filename(filename):
    """Return the filename to store the cached data in."""
    head, tail = os.path.split(filename)
    return os.path.join(
        '.baroness',
        os.path.abspath(head).lstrip(os.path.sep),
        tail + '.json'
    )
