# Baroness

Toolkit for easy searching and manipulation of python source code using
redbaron.

[ ![Codeship Status for Smirl/baroness](https://app.codeship.com/projects/647edcd0-bcc0-0135-7fde-5afd35787ded/status?branch=master)](https://app.codeship.com/projects/259596) [![Coverage Status](https://coveralls.io/repos/github/Smirl/baroness/badge.svg?branch=HEAD)](https://coveralls.io/github/Smirl/baroness?branch=HEAD)

## Installation

	pip install baroness

See https://pypi.python.org/pypi/baroness


## Usage

### Searching

You can search through python code using the redbaron API on the
commandline. By default baroness will search through all python files
from the current directory down recursively. The search pattern is just
regular python code that would work with redbaron. The top level node is
called root.

For example to search for all `name` nodes with a value of `bar`:

	baroness search 'root("name", value="bar")'

`search` is the default subcommand so you can write the same with:

	baroness 'root("name", value="bar")'

For full usage look at `baroness search --help`:

	usage: baroness search [-h] [--no-cache] [--parents PARENTS] [--no-color]
	                       [--no-linenos]
	                       pattern [files [files ...]]

	positional arguments:
	  pattern            Python redbaron code to search where `root` is the
	                     variable holding the tree
	  files              File names and/or glob pattern. Default to recursive
	                     search of python all files.

	optional arguments:
	  -h, --help         show this help message and exit
	  --no-cache         Do no use the cache in `.baroness` even if it exists
	  --parents PARENTS  Number of parents to go up on matched nodes.
	  --no-color         Do not color the output.
	  --no-linenos       Do not output the linenumbers.


### Caching

Parsing python files to a baron fst can be time consuming for large
code bases. Baroness can cache the baron fst as json files to save time
when searching. By default caching isn't enabled, but will be used if
baroness finds a `.baroness` directory.

#### Saving/Initialising Cache

To enable caching (and initially create cache) you can use:

	baroness cache save

For full usage look at `baroness cache save --help`:

	usage: baroness cache save [-h] [--force] [FILE [FILE ...]]

	Save given files (all tree) to disk

	positional arguments:
	  FILE        Files to save to cache.

	optional arguments:
	  -h, --help  show this help message and exit
	  --force     Save over already existing cache files.


#### Clearing the Cache

To delete all `.baroness` directories recursively use:

	baroness cache delete

