"""Test the baroness.util package."""


from redbaron import RedBaron
import pytest

from baroness.utils import format_node


@pytest.fixture
def assignment_node():
    """Return a simple assignment_node."""
    return RedBaron('a = 1')[0]


@pytest.mark.parametrize(
    'no_color, no_linenos, expected',
    [
        (True, False, u'1-a = 1'),
        (True, True, u'a = 1'),
        (
            False,
            False,
            u'\x1b[38;5;141m1\x1b[39m-\x1b[38;5;15ma\x1b[39m\x1b[38;5;15m '
            '\x1b[39m\x1b[38;5;197m=\x1b[39m\x1b[38;5;15m \x1b[39m\x1b[38;'
            '5;141m1\x1b[39m'
        ),
        (
            False,
            True,
            u'\x1b[38;5;15ma\x1b[39m\x1b[38;5;15m \x1b[39m\x1b[38;5;197m=\x1b'
            '[39m\x1b[38;5;15m \x1b[39m\x1b[38;5;141m1\x1b[39m'
        ),
    ]
)
def test_format_node(assignment_node, no_color, no_linenos, expected):
    """Test the format_node output for given inputs."""
    assert format_node(
        assignment_node,
        no_color=no_color,
        no_linenos=no_linenos
    ) == expected


def test_format_node_no_parent(assignment_node):
    """Test the format_node output for given inputs."""
    assignment_node.parent = None
    assert format_node(
        assignment_node,
        no_color=True,
        no_linenos=False
    ) == '**-a = 1'
