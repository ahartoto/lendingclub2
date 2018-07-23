"""
LendingClub2 Response Package
"""

# lendingclub2
from lendingclub2.config import ResponseCode


class Response:
    """
    Base Response class
    """
    def __init__(self, response):
        self._response = response
        self._json = response.json()

    @property
    def json(self):
        """
        Get the JSON body from the response

        :returns: JSON object
        """
        return self._json

    @property
    def request(self):
        """
        Get the request object

        :returns: instance of requests.Request
        """
        return self._response.request

    @property
    def status_code(self):
        """
        Get the status code of the response

        :returns: int
        """
        return self._response.status_code

    @property
    def successful(self):
        """
        Check if the response was a successful one

        :returns: boolean
        """
        return self.status_code == ResponseCode.SUCCESSFUL.value
