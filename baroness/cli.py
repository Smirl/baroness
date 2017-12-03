"""The entry point the baroness command line tool."""


from __future__ import print_function
from argparse import ArgumentParser


def main():
    """The parser and entry point."""
    parser = ArgumentParser('baroness')
    subparsers = parser.add_subparsers()

    cache = subparsers.add_parser('cache', help='Manage FST file cache')
    cache_subparsers = cache.add_subparsers()

    cache_save = cache_subparsers.add_parser('save', help='Save given files (all tree) to disk')
    cache_save.add_argument('files', help='Files and paths to save', default='*')

    args = parser.parse_args()

    print(vars(args))
    return args
