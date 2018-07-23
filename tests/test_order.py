# Filename: test_order.py

"""
Test the lendingclub2.response.order module
"""

# Standard libraries
import collections
import random

# PyTest
import pytest

# lendingclub2
from lendingclub2 import loan
from lendingclub2.account import InvestorAccount
from lendingclub2.authorization import Authorization
from lendingclub2.error import LCError
from lendingclub2.filter import (
    BorrowerEmployedTrait,
    FilterByBorrowerTraits,
    FilterByApproved, FilterByFunded, FilterByGrade, FilterByTerm,
)
from lendingclub2.response.order import Order, OrderNote


class TestOrder:
    def test_order(self):
        try:
            _ = Authorization().key
        except LCError:
            pytest.skip("skip test: cannot find authorization key")

        # Search loans matching our criteria
        listing = loan.Listing()
        listing.search()

        loans = listing.filter(
            FilterByTerm(value=36),
            FilterByGrade(grades='AB'),
            FilterByFunded(percentage=80),
            FilterByApproved(),
        )

        # Now narrow it down to borrowers with specific traits
        traits = (
            BorrowerEmployedTrait(),
        )
        loans = loans.filter(FilterByBorrowerTraits(traits))

        account = InvestorAccount()
        balance = account.available_balance

        # Diversify
        notes = list()
        for selected_loan in loans:
            if balance >= 25:
                note = OrderNote(selected_loan.id, 25)
                balance -= 25
                notes.append(note)
            else:
                break

        if notes:
            order = Order(account.id(), *notes)
            assert order.successful
