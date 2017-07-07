# Filename: test_transfer.py

"""
Test the lendingclub2.response.transfer module
"""

# PyTest
import pytest

# lendingclub2
from lendingclub2.account import InvestorAccount
from lendingclub2.error import LCError
from lendingclub2.response import transfer


class TestTransferFund(object):
    def test_cancel(self):
        try:
            investor = InvestorAccount()
        except LCError:
            pytest.skip("skip test: can't find account info")

        response = transfer.cancel(investor.id())
        assert response is None

    def test_pending(self):
        try:
            investor = InvestorAccount()
        except LCError:
            pytest.skip("skip test: can't find account info")

        response = transfer.pending(investor.id())
        assert response.successful
