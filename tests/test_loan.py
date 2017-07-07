# Filename: test_loan.py

"""
Test the lendingclub2.loan module
"""

# Standard libraries
import collections

# lendingclub2
from lendingclub2 import loan


class TestListing(object):
    def test_search(self):
        listing = loan.Listing()
        listing.search()
        assert isinstance(listing.loans, collections.Iterable)
