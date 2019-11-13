import pytest

from src.util.helpers import exclude_directories

MOCK_OS_WALK = tuple([
    ('home/dir1', [""], [""]),
    ('home/dir2', [""], [""]),
    ('home/dir3', [""], [""]),
    ('home/dir4', [""], [""]),
    ]
)

def test_exclude_some():
    exclude = ["dir1", "dir2"]

    assert exclude_directories(MOCK_OS_WALK, exclude) == tuple([
        ('home/dir3', [""], [""]),
        ('home/dir4', [""], [""]),
        ]
    )

def test_exclude_none():
    exclude = []

    assert exclude_directories(MOCK_OS_WALK, exclude) == tuple([
        ('home/dir1', [""], [""]),
        ('home/dir2', [""], [""]),
        ('home/dir3', [""], [""]),
        ('home/dir4', [""], [""]),
    ])

def test_exclude_empty_string():
    # this should never happen
    exclude = [""]

    with pytest.raises(AssertionError):
        exclude_directories(MOCK_OS_WALK, exclude)

def test_exclude_all():
    exclude = ['dir1', 'dir2', 'dir3', 'dir4']

    assert len(exclude_directories(MOCK_OS_WALK, exclude)) == 0


# def test_indent():
#     input = ("root/1")
#
#     out = indent_items(input)
#
#     assert out == "  root/1"
