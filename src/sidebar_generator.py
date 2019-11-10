"""
Generates a _Sidebar.md that shows a tree of the wiki.
This is mostly useful for gitlab wiki (Gollum) based wikis.
"""

import argparse, os
import logging
from typing import List, Tuple, TypeVar, Any

logging.basicConfig(level=logging.DEBUG)

# Define type that represents results from recursive directory walk.
# The immutable tuple contains tuples in the form of (dir name, list of subdirs, list of files)
dirtuple = TypeVar('dirtuple', bound=Tuple[Tuple[str, List[str], List[str]]])


def parse_args() -> Tuple[List[str], int, List[int], str]:
    """
    Parse external arguments
    :return: tuple of relevant args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--exclude", nargs='+',
                        help='list of directories names to exclude. Includes all subdirectories. Defaults to config '
                             'file exclusions')
    parser.add_argument("--max-depth", help="maximum depth to build tree", default=3, type=int)
    parser.add_argument("--hide-files", action="store_true",
                        help="Only build the sidebar using directories, hiding files")
    parser.add_argument(help="wiki root directory", dest="wiki_root")
    args = parser.parse_args()

    # convert relative paths to absolute path
    root_dir = os.path.abspath(os.path.expanduser(args.wiki_root))

    # todo need to split out? or just return (modified) Namespace object from parse_args?
    return args.exclude, args.max_depth, args.hide_files, root_dir


# UPDATE look into TypeVar?
def exclude_directories(dirs: Tuple[Tuple[str, List[str], List[str]]], excludes: List[str]) \
        -> Tuple[Tuple[str, List[str], List[str]]]:
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


def get_directories(root: str) -> dirtuple:
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


def map_dirtuple_files_to_lines(dirtuples: Any) -> Any:
    """
    Map each dirtuple from (root, [dirs..], [file1, file2, file3] to (root/file1); (root/file2), ..etc
    :param dirtuples: todo
    :return: todo
    """

    # convert each tuple into a list containing the root+/+file for each file in the tuple,
    # append that list onto the root so that the directory name is preserved by itself
    tuples = map(lambda item: [item[0]] + [item[0]+os.sep+file for file in item[2]], dirtuples)

    # flatten the list
    # https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
    tuples_flat = [item for sublist in tuples for item in sublist]

    return tuple(tuples_flat)


def indent_items(items):
    """
    todo
    :param items:
    :return:
    """

    indent = lambda path: (path.count(os.sep) -1) * '  ' + path

    return tuple(map(indent, items))



def main():
    # get args
    excludes, max_depth, hide_files, root_dir = parse_args()

    # log information message for root dir
    logging.info(f"Creating sidebar starting from {root_dir}")

    # get directories
    dirs: tuple = get_directories(root_dir)

    # filter directories
    dirs_filtered = exclude_directories(dirs, excludes)

    # add files to list
    items = map_dirtuple_files_to_lines(dirs_filtered)

    # Remove root dir from each item
    items_removed_root = list(map(lambda line: line.replace(root_dir, ""), items))

    # create indents
    items_indented = indent_items(items_removed_root)


    # celebrate


    for i in items_indented:
        print(i)

if __name__ == '__main__':
    main()
