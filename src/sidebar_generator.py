"""
Generates a _Sidebar.md that shows a tree of the wiki.
This is mostly useful for gitlab wiki (Gollum) based wikis.
"""

import argparse, os, yaml
import logging
from typing import List, Tuple, TypeVar, Any

from util.config_reader import get_wiki_root
from util.helpers import get_directories, exclude_directories, Dir_tuple

logging.basicConfig(level=logging.DEBUG)

# Define type that represents results from recursive directory walk.
# The immutable tuple contains tuples in the form of (dir name, list of subdirs, list of files)
dirtuple = TypeVar('dirtuple', bound=Tuple[Tuple[str, List[str], List[str]]])


def parse_args() -> Tuple[List[str], int, List[int], str]:
    """
    Parse external arguments (contains side effects)
    :return: tuple of relevant args
    :raises
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--exclude", nargs='+',
                        help='list of directories names to exclude. Includes all subdirectories. Defaults to config '
                             'file exclusions')
    parser.add_argument("--max-depth", help="maximum depth to build tree", default=3, type=int)
    parser.add_argument("--hide-files", action="store_true",
                        help="Only build the sidebar using directories, hiding files")
    parser.add_argument("--wiki", help="wiki root directory")
    args = parser.parse_args()

    # convert relative paths to absolute path
    root_dir = os.path.abspath(os.path.expanduser(args.wiki if args.wiki else get_wiki_root()))

    return args.exclude, args.max_depth, args.hide_files, root_dir


def expand_dirtuple_files_to_lines(dirtuples: Dir_tuple) -> Tuple[str]:
    """
    Map each directory tuple to a list item, expanding

    Example:
    input =  ((root, [dirs..], [file1, file2, file3]))
    output = (
        "{root}/{file1}",
        "{root}/{file2}",
        "{root}/{file3}",
    )
    :param dirtuples: inputted Dir Tuple datatype
    :return tuple of strings representing list items
    """

    # convert each tuple into a list containing the root+/+file for each file in the tuple,
    # append that list onto the root so that the directory name is preserved
    tuples = map(lambda item: [item[0]] + [item[0]+os.sep+file for file in item[2]], dirtuples)

    # flatten the list
    # https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
    tuples_flat: List[str] = [item for sublist in tuples for item in sublist]

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
    dirs: Dir_tuple = get_directories(root_dir)

    # filter directories
    dirs_filtered = exclude_directories(dirs, excludes)

    # turn the dir_tuple into a flat list
    items = expand_dirtuple_files_to_lines(dirs_filtered)

    # Remove root dir from each item
    items_removed_root = list(map(lambda line: line.replace(root_dir, ""), items))

    # create indents
    items_indented = indent_items(items_removed_root)

    # celebrate


    for i in items_indented:
        print(i)

if __name__ == '__main__':
    main()
