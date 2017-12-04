"""Utils shared by commands."""

from argparse import _SubParsersAction
from glob import glob
import os
import sys


def filenames(files):
    """
    Yield string filenames given filenames or globs, else walk current dir.

    Input can either be an empty list, meaning we walk the current directory
    and yield python files. Or can be a list of filenames and/or glob patterns
    which we expand, and filter for python files.
    """
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