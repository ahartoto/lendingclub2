# Filename: test_transfer.py

"""
Test the lendingclub2.response.transfer module
"""

# Standard libraries
import collections
import datetime

# PyTest
import pytest

# lendingclub2
from lendingclub2.account import InvestorAccount
from lendingclub2.config import TransferFrequency
from lendingclub2.error import LCError
from lendingclub2.response import transfer


class TestTransferFund:
    def test_add(self):
        try:
            investor = InvestorAccount()
        except LCError:
            pytest.skip("skip test: can't find account info")

        with pytest.raises(LCError):
            transfer.add(investor.id(), 0)

        with pytest.raises(LCError):
            transfer.add(investor.id(), -1)

        with pytest.raises(LCError):
            transfer.add(investor.id(), 1, frequency='FOO')

        with pytest.raises(LCError):
            transfer.add(investor.id(), 1, frequency=TransferFrequency.BIWEEKLY)

        with pytest.raises(LCError):
            transfer.add(investor.id(), 1,
                         frequency=TransferFrequency.BIWEEKLY,
                         start_date='foo')

        with pytest.raises(LCError):
            transfer.add(investor.id(), 1,
                         frequency=TransferFrequency.BIWEEKLY,
                         start_date=datetime.datetime.now(),
                         end_date='foo')

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

        txns = transfer.pending(investor.id())
        assert isinstance(txns, collections.abc.Iterable)

    def test_withdrawal(self):
        try:
            investor = InvestorAccount()
        except LCError:
            pytest.skip("skip test: can't find account info")

        with pytest.raises(LCError):
            transfer.withdraw(investor.id(), 0)

        with pytest.raises(LCError):
            transfer.withdraw(investor.id(), -1)
