"""
Generates a _Sidebar.md that shows a tree of the wiki.
This is mostly useful for gitlab wiki (Gollum) based wikis.
"""

import argparse



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--exclude", nargs='+', help='list of directories names to exclude. Includes all subdirectories. Defaults to config file exclusions')
    parser.add_argument("--max-depth", help="maximum depth to build tree", default=3)
    parser.add_argument("--hide-files", action="store_true", help="Only build the sidebar using directories, hiding files")
    parser.add_argument("wiki-root", help="wiki root directory")
    args = parser.parse_args()

