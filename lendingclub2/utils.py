# Filename: utils.py

"""
LendingClub2 Utilities Module

Interface functions:
    get_config_content
    get_config_fpath
"""

# Standard libraries
import os
from configparser import ConfigParser

# lendingclub2
from lendingclub2.config import CONFIG_FPATH, CONFIG_FPATH_ENV
from lendingclub2.error import LCError


# Interface functions
def get_config_content():
    """
    Read the configuration file content

    :returns: instance of configparser.ConfigParser
    """
    fpath = get_config_fpath()
    if not os.path.exists(fpath):
        fstr = "expected configuration path doesn't exist: " + fpath
        raise LCError(fstr)

    config = ConfigParser()
    with open(fpath) as fin:
        config.read_file(fin)
    return config


def get_config_fpath():
    """
    Get the configuration file path

    :returns: string
    """
    if os.getenv(CONFIG_FPATH_ENV, None) is None:
        fpath = CONFIG_FPATH
    else:
        fpath = os.getenv(CONFIG_FPATH_ENV)
    return fpath
