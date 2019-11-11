"""
Config reader parses YAML config file and returns data
"""

import yaml, os
from pathlib import Path


def get_project_root() -> Path:
    """
    Get project root directory
    :return: Path
    """

    return Path(__file__).parent.parent


def get_wiki_root():
    """
    :return wiki root directory
    :raise IOError if directory not found
    :raise YAMLError if root directory isn't in config
    """

    # sanity check
    if 'root_dir' not in config:
        raise yaml.YAMLError("root_dir not in config file")

    # return path if valid, otherwise raise an exception
    if os.path.isdir(config['root_dir']):
        return config['root_dir']

    raise IOError(f"Invalid or unknown directory {config['root_dir']}")


# try open and validate yaml file, raising error if failed
with open(os.path.join(get_project_root(), "config.yml"), 'r') as stream:
    config = yaml.load(stream) or {}
