"""Test that version in version.txt if unique when we deploy."""


from collections import namedtuple
from functools import total_ordering
import os
import subprocess
import re


SEMVER_REGEX = re.compile('^(\d+)\.(\d+)\.(\d+)$')


@total_ordering
class Version(namedtuple('Version', 'major minor patch')):
    """A namedtuple with semver ordering."""

    def __eq__(self, other):
        """Compare the parts."""
        return (
            (self.major == other.major) and
            (self.minor == other.minor) and
            (self.patch == other.patch)
        )

    def __gt__(self, other):
        """Compare versions by their parts."""
        return (
            (self.major > other.major) or
            (self.major == other.major and self.minor > other.minor) or
            (self.major == other.major and self.minor == other.minor and self.patch > other.patch)
        )

    def __str__(self):
        """The original string hopefully."""
        return '.'.join([self.major, self.minor, self.patch])


def main():
    """Get the latest git tag and compare to version.txt."""
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'baroness', 'version.txt')
    with open(path) as f:
        current_version = Version(*f.read().strip().split('.'))

    tags = subprocess.check_output(['git', 'tag']).splitlines()
    latest_version = next(iter(sorted(
        (Version(*SEMVER_REGEX.match(tag).groups()) for tag in tags if SEMVER_REGEX.match(tag)),
        reverse=True
    )))

    assert str(current_version) not in tags, '{} is in {}'.format(current_version, tags)
    assert current_version > latest_version, '{} not greater than {}'.format(current_version, latest_version)


if __name__ == '__main__':
    main()
