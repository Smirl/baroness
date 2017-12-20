"""The entry point the baroness command line tool."""


from __future__ import print_function
from argparse import ArgumentParser
import multiprocessing
import logging

from baroness.cache import cache_save, cache_delete
from baroness.search import search
from baroness.utils import set_default_subparser, LOGGER


def main():
    """The parser and entry point."""
    ArgumentParser.set_default_subparser = set_default_subparser
    parser = ArgumentParser('baroness')
    sub = parser.add_subparsers()

    # Cache
    cache_parser = sub.add_parser('cache')
    cache_sub = cache_parser.add_subparsers()

    cache_save_parser = cache_sub.add_parser(
        'save',
        description='Save given files (all tree) to disk'
    )
    cache_save_parser.add_argument(
        'files',
        nargs='*',
        metavar='FILE',
        help='Files to save to cache.'
    )
    cache_save_parser.add_argument(
        '--force',
        action='store_true',
        help='Save over already existing cache files.'
    )
    cache_save_parser.set_defaults(func=cache_save)

    cache_del_parser = cache_sub.add_parser(
        'delete',
        description='Remove all .baroness directories'
    )
    cache_del_parser.set_defaults(func=cache_delete)

    # Search
    search_parser = sub.add_parser('search')
    search_parser.add_argument(
        'pattern',
        help='Python redbaron code to search where `root` is the variable holding the tree'
    )
    search_parser.add_argument(
        'files',
        nargs='*',
        help='File names and/or glob pattern. Default to recursive search of python all files.'
    )
    search_parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Do no use the cache in `.baroness` even if it exists'
    )
    search_parser.add_argument(
        '--parents',
        default=0,
        type=int,
        help='Number of parents to go up on matched nodes.'
    )
    search_parser.add_argument(
        '--no-color',
        action='store_true',
        help='Do not color the output.'
    )
    search_parser.add_argument(
        '--no-linenos',
        action='store_true',
        help='Do not output the linenumbers.'
    )
    search_parser.add_argument(
        '-v', '--verbose',
        default=0,
        action='count',
        help='Level of verbosity. Can be used many times.'
    )
    search_parser.add_argument(
        '-P', '--processes',
        default=multiprocessing.cpu_count() + 1,  # 'cus why not
        type=int,
        help='Number of processes to use.'
    )
    search_parser.set_defaults(func=search)

    parser.set_default_subparser('search')

    args = vars(parser.parse_args())
    func = args.pop('func')
    if args.get('verbose', 0) > 0:
        LOGGER.setLevel(logging.DEBUG)
    return func(**args)
