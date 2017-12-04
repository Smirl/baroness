"""Handle caching of FST to json."""

from __future__ import print_function
import shutil
import os

from distutils.dir_util import mkpath
from redbaron import RedBaron

from baroness.utils import filenames

try:
    import ujson as json
except ImportError:
    import json


def cache_save(files, force):
    """Go through a save the baron FST to .baroness directory."""
    if not os.path.exists('.baroness'):
        os.mkdir('.baroness')

    for filename in filenames(files):
        cache_file = os.path.join('.baroness', filename) + '.json'
        mkpath(os.path.split(cache_file)[0])

        if not force and os.path.exists(cache_file):
            print('Skipping cached file', filename)
            continue

        with open(filename) as py, open(cache_file, 'w') as output:
            json.dump(RedBaron(py.read()).fst(), output)
        print('Saved', filename, 'fst to', cache_file)


def cache_delete():
    """Remove the .baroness cache directory."""
    shutil.rmtree('.baroness')
    print('Removing cache in', os.path.abspath('.baroness'))
