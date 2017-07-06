# Filename: summary.py

"""
LendingClub2 Summary Response Module
"""

# lendingclub2
from lendingclub2 import requests
from lendingclub2.config import API_VERSION, DNS, ENDPOINTS
from lendingclub2.response import Response


class Summary(Response):
    """
    Get the response of summary endpoint
    """
    def __init__(self, investor_id):
        url = DNS + ENDPOINTS['summary'].format(version=API_VERSION,
                                                investor_id=investor_id)
        response = requests.get(url)
        Response.__init__(self, response)
