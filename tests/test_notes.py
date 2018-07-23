# Filename: test_notes.py

"""
Test the lendingclub2.response.notes module
"""

# PyTest
import pytest

# lendingclub2
from lendingclub2.account import InvestorAccount
from lendingclub2.error import LCError
from lendingclub2.response.notes import Notes


class TestNotes:
    def test_properties(self):
        investor_id = None
        try:
            investor_id = InvestorAccount.id()
        except LCError:
            pytest.skip("skip because cannot find account ID")

        notes = Notes(investor_id)
        assert notes.successful
        assert len(notes) >= 0
