"""
Collection of helper functions that are common to the sidebar and contents generation scripts
"""

from typing import Tuple, List
import os

# Define alias for dir tuples, which are an immutable list of tuples of the form (root, dirs, files).
# Where root is the directory name, and dirs and files exist within the directory
Dir_tuple = Tuple[Tuple[str, List[str], List[str]]]


def exclude_directories(dirs: Dir_tuple, excludes: List[str]) -> Dir_tuple:
    """
    Exclude a set of directories from the original list
    :param dirs: list of directories
    :param excludes: list of directories to exclude
    :return: list with excluded directories
    """

    assert not any(x == "" for x in excludes), "excludes contains empty string"

    # exclude directories that have an "excluded directory" in them
    # use os.set + dir to look for parts of the string like "/images"
    return tuple(filter(lambda x: not any(os.sep + _dir in x[0] for _dir in excludes), dirs))


def get_directories(root: str) -> Dir_tuple:
    """
    :return immutable list of 3 element tuples representing the directory, directory folders and directory files for each
    sub-directory within the root directory.
    :param root: directory where to start the recursive search from
    """

    # sort dirs and files in place so that os.walk recurses into them in alphabetical order
    # https://stackoverflow.com/questions/6670029/can-i-force-python3s-os-walk-to-visit-directories-in-alphabetical-order-how
    dirs = []
    for path, subdirs, files in os.walk(root):
        subdirs.sort()
        files.sort()
        dirs.append((path, subdirs, files))

    return tuple(dirs)
