# Filename: portfolio.py

"""
LendingClub2 Response Portfolio Module
"""

# lendingclub2
from lendingclub2 import request
from lendingclub2.config import API_VERSION, DNS, ENDPOINTS
from lendingclub2.response import Response


class Portfolio:
    """
    Get a representation of portfolio
    """

    def __init__(self, investor_id, response=None):
        """
        Constructor

        :param investor_id: int
        :param response: JSON object
        """
        self._investor_id = investor_id
        self._response = response

    def create(self, name, description=None):
        """
        Create a new portfolio

        :param name: string - name of portfolio
        :param description: string - description of portfolio (default: None)
        """
        payload = {
            'actorId': self._investor_id,
            'portfolioName': name,
        }
        if description is not None:
            payload['portfolioDescription'] = description

        response = request.post(self.url, json=payload)
        self._response = Response(response)

    @property
    def description(self):
        """
        Get the new portfolio description. If no description, it's an empty
        string.

        :returns: string
        """
        return self.json['portfolioDescription'] or ''

    @property
    def id(self):
        """
        Get the new portfolio ID

        :returns: int
        """
        return self.json['portfolioId']

    @property
    def json(self):
        """
        Get the JSON representation of the portfolio

        :returns: JSON object
        """
        if isinstance(self._response, Response):
            return self._response.json
        return self._response

    @property
    def name(self):
        """
        Get the new portolio name

        :returns: string
        """
        return self.json['portfolioName']

    @property
    def url(self):
        """
        Get the relevant URL

        :returns: string
        """
        return DNS + ENDPOINTS['portfolios'].format(
            version=API_VERSION, investor_id=self._investor_id)


class Portfolios(Response):
    """
    Get the list of portfolios for a given account
    """

    def __init__(self, investor_id):
        """
        Constructor

        :param investor_id: int
        """
        self._investor_id = investor_id
        response = request.get(self.url)
        Response.__init__(self, response)

        # Formulate the list of portfolios
        self._list = list()
        if 'myPortfolios' in self.json:
            for portfolio_json in self.json['myPortfolios']:
                self._list.append(Portfolio(self._investor_id,
                                            response=portfolio_json))

    def __contains__(self, item):
        """
        Check if portfolio ID is in the list

        :param item: int - portfolio ID
        :returns: boolean
        """
        for portfolio in self:
            if portfolio.id == item:
                return True
        return False

    def __iter__(self):
        """
        Get the iterable representation of the instance

        :returns: iterable
        """
        return iter(self._list)

    def __len__(self):
        """
        Get number of portfolios

        :returns: int
        """
        return len(self._list)

    @property
    def url(self):
        """
        Get the relevant URL

        :returns: string
        """
        return DNS + ENDPOINTS['portfolios'].format(
            version=API_VERSION, investor_id=self._investor_id)
