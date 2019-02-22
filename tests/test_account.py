# Filename: test_account.py

"""
Test the lendingclub2.accountmodule
"""

# Standard libraries
from unittest import mock

# requests
import requests

# lendingclub2
from lendingclub2 import account
from lendingclub2.response import summary


_CONFIG = {
    'account': {
        'investor_id': 'fake_investor_id',
    },
    'access': {
        'api_key': 'fake_api_key',
    },
}

_RESPONSES = {
    'valid': r'{"availableCash": 1.25, "accountTotal": 1.26}',
}


class TestInvestorAccount:
    def teardown_method(self):
        """Remove stored account ID."""
        account.InvestorAccount._ID = None

    @mock.patch.object(account.utils, 'get_config_content')
    @mock.patch.object(summary.request, 'get')
    def test_properties(self, request_mock, config_mock):
        # Auth setup
        config_mock.return_value = _CONFIG

        # Summary setup
        response = requests.Response()
        response.status_code = requests.codes.ok
        response._content = str.encode(_RESPONSES['valid'])
        request_mock.return_value = response

        investor = account.InvestorAccount()

        # Mocks are called
        assert config_mock.called
        assert request_mock.called

        # Tests
        assert investor.available_balance == 1.25
        assert investor.total_balance == 1.26
