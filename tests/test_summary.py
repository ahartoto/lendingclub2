# Filename: test_summary.py

"""
Test the lendingclub2.response.summary module
"""

# PyTest
import pytest

# lendingclub2
from lendingclub2.account import InvestorAccount
from lendingclub2.error import LCError
from lendingclub2.response.summary import Summary


class TestSummary(object):
    def test_properties(self):
        investor_id = None
        try:
            investor_id = InvestorAccount.id()
        except LCError:
            pytest.skip("skip because cannot find account ID")

        summary = Summary(investor_id)
        assert summary.successful
        assert summary.available_cash >= 0.0
        assert summary.account_total >= 0.0
