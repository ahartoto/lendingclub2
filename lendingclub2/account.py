# Filename: account.py

"""
LendingClub2 Account Module

Interface classes:
    InvestorAccount
"""

# lendingclub2
from lendingclub2 import utils
from lendingclub2.error import LCError
from lendingclub2.response.notes import Notes
from lendingclub2.response.summary import Summary


class InvestorAccount(object):
    """
    Representation of an investor account in Lending Club
    """
    _ID = None

    def __init__(self):
        """
        Constructor
        """
        self._summary = Summary(InvestorAccount.id())
        self._notes = Notes(InvestorAccount.id())

    @classmethod
    def id(cls):
        """
        Get the account ID

        :returns: string
        """
        if cls._ID is None:
            config = utils.get_config_content()
            try:
                cls._ID = config['account']['investor_id']
            except KeyError as exc:
                fstr = "cannot find the information of the investor ID"
                raise LCError(fstr, hint=str(exc))
        return cls._ID

    @property
    def notes(self):
        """
        Get the notes associated with the account

        :returns: instance of lendingclub2.response.Notes
        """
        return self._notes

    @property
    def available_balance(self):
        """
        Get the amount of cash that's available

        :returns: float
        """
        return self._summary.available_cash

    @property
    def total_balance(self):
        """
        Get the total balance of the account

        :returns: float
        """
        return self._summary.account_total
