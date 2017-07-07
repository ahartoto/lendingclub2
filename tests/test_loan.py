# Filename: test_loan.py

"""
Test the lendingclub2.loan module
"""

# Standard libraries
import collections

# PyTest
import pytest

# lendingclub2
from lendingclub2 import loan
from lendingclub2.authorization import Authorization
from lendingclub2.error import LCError


class TestListing(object):
    def test_search(self):
        try:
            _ = Authorization.key
        except LCError:
            pytest.skip("skip test: cannot find authorization key")

        listing = loan.Listing()
        listing.search()
        assert isinstance(listing.loans, collections.Iterable)
