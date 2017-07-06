# Filename: authorization.py

"""
LendingClub2 Authorization Module
"""

# Standard libraries
import os
from configparser import ConfigParser

# lendingclub2
from lendingclub2.config import API_KEY_ENV, CONFIG_FPATH, CONFIG_FPATH_ENV
from lendingclub2.error import LCError


class Authorization(object):
    """
    Get the authorization information
    """
    _CODE = None

    def __init__(self):
        if Authorization._CODE is not None:
            return

        if os.getenv(API_KEY_ENV):
            Authorization._CODE = os.getenv(API_KEY_ENV)
        else:
            if os.getenv(CONFIG_FPATH_ENV, None) is None:
                fpath = CONFIG_FPATH
            else:
                fpath = os.getenv(CONFIG_FPATH_ENV)

            if not os.path.exists(fpath):
                fstr = "expected configuration path doesn't exist: " + fpath
                raise LCError(fstr)

            config = ConfigParser()
            with open(fpath) as fin:
                config.read_file(fin)

            try:
                Authorization._CODE = config['access']['api_key']
            except KeyError as exc:
                fstr = "configuration file doesn't have info about api_key"
                raise LCError(fstr, hint=str(exc))

    @property
    def key(self):
        """
        Get the authorization key

        :returns: string
        """
        return Authorization._CODE

    @property
    def header(self):
        """
        Get the header to be added to request

        :returns: dict
        """
        return {'Authorization': Authorization.key}
