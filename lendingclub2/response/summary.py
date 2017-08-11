# Filename: summary.py

"""
LendingClub2 Summary Response Module

Interface classes:
    Summary
"""

# lendingclub2
from lendingclub2 import request
from lendingclub2.config import API_VERSION, DNS, ENDPOINTS
from lendingclub2.response import Response


class Summary(Response):
    """
    Get the response of summary endpoint
    """
    def __init__(self, investor_id):
        """
        Constructor

        :param investor_id: int
        """
        self._investor_id = investor_id
        response = request.get(self.url)
        Response.__init__(self, response)

    @property
    def available_cash(self):
        """
        Get all the available cash amount

        :returns: float
        """
        return self.json['availableCash']

    @property
    def account_total(self):
        """
        Get the account total

        :returns: float
        """
        return self.json['accountTotal']

    @property
    def url(self):
        """
        Find the relevant url

        :returns: string
        """
        url = DNS + ENDPOINTS['summary'].format(version=API_VERSION,
                                                investor_id=self._investor_id)
        return url

    def update(self):
        """
        Update the summary
        """
        self._response = request.get(self.url)
