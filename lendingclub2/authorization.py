# Filename: authorization.py

"""
LendingClub2 Authorization Module
"""

# Standard libraries
import os

# lendingclub2
from lendingclub2 import utils
from lendingclub2.config import API_KEY_ENV
from lendingclub2.error import LCError


class Authorization:
    """
    Get the authorization information
    """
    _CODE = None

    def __init__(self):
        """
        Constructor
        """
        if Authorization._CODE is not None:
            return

        if os.getenv(API_KEY_ENV):
            Authorization._CODE = os.getenv(API_KEY_ENV)
        else:
            config = utils.get_config_content()
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
        return {'Authorization': self.key}
