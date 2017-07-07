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
from lendingclub2 import filter
from lendingclub2 import loan
from lendingclub2.authorization import Authorization
from lendingclub2.error import LCError


class TestListing(object):
    def test_search(self):
        try:
            _ = Authorization().key
        except LCError:
            pytest.skip("skip test: cannot find authorization key")

        listing = loan.Listing()
        listing.search()
        assert isinstance(listing.loans, collections.Iterable)

        grade = random.choice('ABCDEFG')
        loans = listing.filter(filter.FilterByGrade(grade))
        assert isinstance(loans, collections.Iterable)
        assert len(loans) >= 0
        for selected_loan in loans:
            assert selected_loan.grade == grade

        term = 36
        loans = listing.filter(filter.FilterByTerm(value=term))
        assert len(loans) >= 0
        for selected_loan in loans:
            assert selected_loan.term == term

        # Chain the filters
        loans = listing.filter(filter.FilterByGrade(grade),
                               filter.FilterByTerm(value=term))
        new_loans = listing.filter(filter.FilterByGrade(grade)).filter(
            filter.FilterByTerm(value=term))
        assert loans == new_loans
