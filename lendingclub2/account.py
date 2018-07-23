# Filename: account.py

"""
LendingClub2 Account Module

Interface classes:
    InvestorAccount
"""

# Standard libraries
import os

# lendingclub2
from lendingclub2 import utils
from lendingclub2.config import INVESTOR_ID_ENV
from lendingclub2.error import LCError
from lendingclub2.response.notes import Notes
from lendingclub2.response.order import Order
from lendingclub2.response.portfolio import Portfolios
from lendingclub2.response.summary import Summary


class InvestorAccount:
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
        self._portfolios = Portfolios(InvestorAccount.id())

    @classmethod
    def id(cls):
        """
        Get the account ID

        :returns: string
        """
        if cls._ID is None:
            if os.getenv(INVESTOR_ID_ENV):
                cls._ID = os.getenv(INVESTOR_ID_ENV)
            else:
                config = utils.get_config_content()
                try:
                    cls._ID = config['account']['investor_id']
                except KeyError as exc:
                    fstr = "cannot find the information of the investor ID"
                    raise LCError(fstr, hint=str(exc))
        return cls._ID

    @property
    def available_balance(self):
        """
        Get the amount of cash that's available

        :returns: float
        """
        return self._summary.available_cash

    @property
    def notes(self):
        """
        Get the notes associated with the account

        :returns: instance of lendingclub2.response.notes.Notes
        """
        return self._notes

    @property
    def portfolios(self):
        """
        Get the portfolios associated with the account

        :returns: instance of lendingclub2.response.portfolio.Portfolios
        """
        return self._portfolios

    @property
    def total_balance(self):
        """
        Get the total balance of the account

        :returns: float
        """
        return self._summary.account_total

    def invest(self, *order_notes):
        """
        Invest to loans as specified

        :param order_notes: iterable of instance of
                            lendingclub2.response.order.OrderNote
        """
        order = Order(self.id(), *order_notes)
        if not order.successful:
            fstr = "could not complete the request completely"
            raise LCError(fstr)
