# Filename: account.py

"""
LendingClub2 Account Module
"""


class Account(object):
    """
    Representation of an account in Lending Club
    """
    investor_id = None

    def __init__(self):
        """
        Constructor
        """
        pass

    @property
    def balance(self):
        """
        Get the current balance of the account

        :returns: float
        """
        return 0.0

    @property
    def id(self):
        """
        Get the account ID

        :returns: string
        """
        return self.investor_id
