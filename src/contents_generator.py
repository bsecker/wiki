"""
Recursively Generates "contents pages" which show the files
and folders within the current directory.
The files are named the same as the folder name so that gitlab wiki
displays them properly.
"""

import logging, os, argparse
from typing import List, Tuple, TypeVar, Any

logging.basicConfig(level=logging.DEBUG)

def parse_args():
    """
    Parse external arguments
    :return:
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--readme", help="Name each file README.md")
    parser.add_argument(help="wiki root directory", dest="wiki_root")

    args = parser.parse_args()

    # convert relative paths to absolute path
    root_dir:str = os.path.abspath(os.path.expanduser(args.wiki_root))

    return root_dir, args.readme


def exclude_directories(dirs: Tuple[Tuple[str, List[str], List[str]]],
                        excludes: List[str]):
    """
    Exclude a set of directories from the original list
    :return:
    """

    assert not any(x == "" for x in excludes), "excludes contains empty string"

    # exclude directories that have an "excluded directory" in them
    # use os.set + dir to look for parts of the string like "/images"
    return tuple(filter(lambda x: not any(os.sep + _dir in x[0] for _dir in excludes), dirs))

def get_directories(root: str):
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

    # can't do it this way
    # dirs = [(root, sorted(dirs), items) for root, dirs, items in os.walk(root, topdown=True)]

    return tuple(dirs)

def main():
    # get the args
    root_dir, readme = parse_args()

    logging.info(f"creating contents starting from {root_dir}")

    # get directories

if __name__ == "__main__":
    main()