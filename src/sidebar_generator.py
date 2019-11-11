"""
Generates a _Sidebar.md that shows a tree of the wiki.
This is mostly useful for gitlab wiki (Gollum) based wikis.
"""

import argparse, os, yaml
import functools
import logging
from typing import List, Tuple, Any

from util.config_reader import get_wiki_root
from util.helpers import get_directories, exclude_directories, Dir_tuple

logging.basicConfig(level=logging.DEBUG)


def parse_args() -> Tuple[List[str], int, List[int], str, bool]:
    """
    Parse external arguments (contains side effects)
    :return: tuple of relevant args
    :raises
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--exclude", nargs='+',
                        help='list of directories names to exclude. Includes all subdirectories. Defaults to config '
                             'file exclusions')
    parser.add_argument("--max-depth", help="maximum depth to build tree", default=10, type=int)
    parser.add_argument("--hide-files", action="store_true",
                        help="Only build the sidebar using directories, hiding files")
    parser.add_argument("--save", action="store_true",
                        help="save to _Sidebar.md in wiki directory, instead out outputting to stdout")
    parser.add_argument("--wiki", help="wiki root directory")
    args = parser.parse_args()

    # convert relative paths to absolute path
    root_dir = os.path.abspath(os.path.expanduser(args.wiki if args.wiki else get_wiki_root()))

    return args.exclude, args.max_depth, args.hide_files, root_dir, args.save


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
    tuples = map(lambda item: [item[0]] + [item[0] + os.sep + file for file in item[2]], dirtuples)

    # flatten the list
    # https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
    tuples_flat: List[str] = [item for sublist in tuples for item in sublist]

    return tuple(tuples_flat)


def indent_items(items: Tuple[str]) -> Tuple[str]:
    """
    Left-pad and add bullet point to each item in the tuple by the number of slashes in the path
    :param items: un-indented list
    :return: indented list
    """

    # convert path to indented version
    indented: Tuple[str] = tuple(map(lambda path: ((path.count(os.sep) - 1) * '  ') + '- ' + path, items))

    return indented


def map_to_links(links: Tuple[str]) -> Tuple[str]:
    """
    Map each item in the tuple to a markdown style link with the label being the end of the path
    :param links:
    :return:
    """

    def convert(item: str):
        item = item.replace(".md", "")
        label = os.path.basename(item)
        return f"[{label}]({item})"

    return tuple(map(convert, links))

def filter_files(hide_files: bool, items: Tuple[str]) -> Tuple[str]:
    """
    Only return directories from the given :param items list.
    :param hide_files: boolean flag from configuration
    :return: new directories
    """
    if hide_files:
        return tuple(filter(lambda item: os.path.isdir(item), items))
    return items


def filter_contents_pages(items: Tuple[str]) -> Tuple[str]:
    """
    Filter out files that have the same name as the directory they are in.
    For example, filter out /root/example/example.md

    This is used because gitlab wiki ui doesn't like folders
    :param items: original list
    :return: modified list with items removed
    """

    def filter_duplicates(item):

        # only filter out files
        if not os.path.isfile(item):
            return True

        # get filename from end of path by splitting away extension(s)
        filename = os.path.basename(item).split(".")[0]

        # get directory name
        directory = os.path.dirname(item)

        return not directory.endswith(filename)

    return tuple(filter(filter_duplicates, items))


def main():
    # get args
    excludes, max_depth, hide_files, root_dir, save = parse_args()

    # log information message for root dir
    logging.info(f"Creating sidebar starting from {root_dir}")

    # get directories
    dirs: Dir_tuple = get_directories(root_dir)

    # filter directories
    dirs_filtered = exclude_directories(dirs, excludes)

    # turn the dir_tuple into a flat list
    items = expand_dirtuple_files_to_lines(dirs_filtered)

    # Filter files
    items_filtered_files = filter_files(hide_files, items)

    # Filter "contents pages" out
    # items_contents_removed = filter_contents_pages(items_filtered_files)

    # for i in items_contents_removed:
    #     print(i)

    # Remove root dir from each item
    items_removed_root = tuple(map(lambda line: line.replace(root_dir, ""), items_filtered_files))

    # Filter to max level
    items_filtered_level = tuple(filter(lambda line: line.count(os.sep) <= max_depth, items_removed_root))

    # turn each item into links
    items_links = map_to_links(items_filtered_level)

    # create indents
    items_indented = indent_items(items_links)

    # add new lines
    items_newlines = tuple(map(lambda x: x + '\n', items_indented))

    # save to file, or print to console
    if save:
        with open(os.path.join(root_dir, "_Sidebar.md"), "w") as f:
            f.writelines(items_newlines)
            logging.info(f"Wrote to _Sidebar.md in {root_dir}")
    else:
        for i in items_newlines:
            # don't add newlines because they are already added earlier
            print(i, end="")


if __name__ == '__main__':
    main()
