# Baroness

Toolkit for easy searching and manipulation of python source code using
redbaron.


## Installation

	pip install baroness


## Usage

### Searching

You can search through python code using the redbaron API on the
commandline. By default baroness will search through all python files
from the current directory down recursively. The search pattern is just
regular python code that would work with redbaron. The top level node is
called root.

For example to search for all `name` nodes with a value of `bar`:

	baroness 'root("name", value="bar")'


### Caching

Parsing python files to a baron fst can be time consuming for large
code bases. Baroness can cache the baron fst as json files to save time
when searching. By default caching isn't enabled, but will be used if
baroness finds a `.baroness` directory.

To enable caching (and initially create cache) you can use:

	baroness cache init

To delete all `.baroness` directories recursively use:

	baroness cache delete
