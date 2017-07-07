# Filename: test_loan.py

"""
Test the lendingclub2.loan module
"""

# Standard libraries
import collections
import random

# PyTest
import pytest

# lendingclub2
from lendingclub2 import loan
from lendingclub2.authorization import Authorization
from lendingclub2.error import LCError
from lendingclub2.filter import FilterByGrade


class TestListing(object):
    def test_search(self):
        try:
            _ = Authorization().key
        except LCError:
            pytest.skip("skip test: cannot find authorization key")

        listing = loan.Listing()
        listing.search()
        assert isinstance(listing.loans, collections.Iterable)

        grade = random.choice('ABCDE')
        loans = listing.filter(FilterByGrade(grade))
        assert isinstance(loans, collections.Iterable)
        assert len(loans) >= 0
        for selected_loan in loans:
            assert selected_loan.grade == grade
