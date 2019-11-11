"""
Recursively Generates "contents pages" which show the files
and folders within the current directory.
The files are named the same as the folder name so that gitlab wiki
displays them properly.
"""

import logging, os, argparse
from typing import List, Tuple, TypeVar, Any

from util.config_reader import get_wiki_root
from util.helpers import exclude_directories, get_directories, Dir_tuple

logging.basicConfig(level=logging.DEBUG)

def parse_args():
    """
    Parse external arguments
    :return:
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--readme", help="Name each file README.md", action="store_true")
    parser.add_argument("--exclude", nargs='+', default=[],
                        help='list of directories names to exclude. Includes all subdirectories. Defaults to config '
                             'file exclusions')
    parser.add_argument("--wiki", help="wiki root directory")

    args = parser.parse_args()

    # convert relative paths to absolute path
    root_dir = os.path.abspath(os.path.expanduser(args.wiki if args.wiki else get_wiki_root()))

    return root_dir, args.readme, args.exclude


def main():
    # get the args
    root_dir, readme, excludes = parse_args()

    logging.info(f"creating contents starting from {root_dir}")

    # get directories
    directories: Dir_tuple  = get_directories(root_dir)

    # filter some directories
    directories_filtered: Dir_tuple = exclude_directories(directories, excludes)

    for root, dirs, files in directories_filtered:

        # get path of each file to write to
        filename = os.path.basename(os.path.normpath(root))
        file_path = f"{root}/{filename}.md" if not readme else f"{root}/README.md"

        # make link for directories - link to the contents page within subdirectory
        dirs_text = map(lambda dir: f" - **[{dir}](./{dir+'/'+dir})**\n", dirs)

        # filter to markdown fiels and remove .md extension in link
        files_text = map(lambda file: f" - [{file[:-3]}]({file[:-3]})", filter(lambda file: file.endswith(".md"), files))

        # add dirs and files to text
        contents = "## Subpages \n"
        for i in dirs_text:
            contents += i + '\n'
        for i in files_text:
            contents += i + '\n'

        contents += "<!-- WARNING: auto generated contents page. Do not edit as it will get overwritten -->\n"

        # write text to the file
        with open(file_path, 'w') as file:
            file.write(contents)
            logging.info("wrote to " + file_path)

if __name__ == "__main__":
    main()