# Filename: test_account.py

"""
Test the lendingclub2.accountmodule
"""

# PyTest
import pytest

# lendingclub2
from lendingclub2.account import InvestorAccount
from lendingclub2.error import LCError


class TestInvestorAccount(object):
    def test_properties(self):
        try:
            investor = InvestorAccount()
        except LCError:
            pytest.skip("skip because cannot find account ID")

        assert investor.available_balance >= 0.0
        assert investor.total_balance >= 0.0
