"""Handle caching of FST to json."""

from __future__ import print_function
import shutil
import os

from baroness.utils import filenames, _load_and_save, _cache_filename


def cache_save(files, force):
    """Go through a save the baron FST to .baroness directory."""
    if not os.path.exists('.baroness'):
        os.mkdir('.baroness')

    for filename in filenames(files):
        cache_file = _cache_filename(filename)
        if not force and os.path.exists(cache_file):
            print('Skipping cached file', filename)
            continue
        _load_and_save(filename, cache_file)
        print('Saved', filename, 'fst to', cache_file)


def cache_delete():
    """Remove the .baroness cache directory."""
    shutil.rmtree('.baroness')
    print('Removing cache in', os.path.abspath('.baroness'))
