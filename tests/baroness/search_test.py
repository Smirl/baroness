"""Test the search functionality."""

import logging

import pytest

from baroness.search import search
from baroness.utils import LOGGER

LOGGER.setLevel(logging.DEBUG)


@pytest.fixture
def workdir(tmpdir):
    """
    A place to add files to search.

    Create a directory called package/
    """
    tmpdir.mkdir('package')
    return tmpdir


@pytest.fixture
def python_file(workdir):
    """Set up temporary files and return the tmpdir."""
    workdir.join('main.py').write('''print("hello")\n''')


def test_search(workdir, python_file, capsys):
    """Test the standard code path which yeilds results."""
    search([str(workdir)], 'root("name")', verbose=1)
