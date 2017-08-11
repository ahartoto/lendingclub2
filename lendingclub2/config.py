# Filename: config.py

"""
LendingClub2 Config Module

Interface enums:
    ResponseCode
    TransferFrequency
"""

# Standard libraries
import os
from enum import Enum


# Constants
API_KEY_ENV = 'LENDING_CLUB_API_KEY'
API_VERSION = 'v1'

CONFIG_FPATH = os.path.expanduser(os.path.join('~', '.lendingclub'))
CONFIG_FPATH_ENV = 'LENDING_CLUB_CONFIG'

DNS = 'https://api.lendingclub.com'

ENDPOINTS = {
    'summary': '/api/investor/{version}/accounts/{investor_id}/summary',
    'available_cash': '/api/investor/{version}/accounts'
                      '/{investor_id}/availablecash',
    'transfer': '/api/investor/{version}/accounts'
                '/{investor_id}/funds/add',
    'withdraw': '/api/investor/{version}/accounts'
                '/{investor_id}/funds/withdraw',
    'pending_transfer': '/api/investor/{version}/accounts'
                        '/{investor_id}/funds/pending',
    'cancel_transfer': '/api/investor/{version}/accounts'
                       '/{investor_id}/funds/cancel',
    'notes': '/api/investor/{version}/accounts/{investor_id}/notes',
    'detailed_notes': '/api/investor/{version}/accounts/'
                      '{investor_id}/detailednotes',
    'portfolios': '/api/investor/{version}/accounts/{investor_id}/portfolios',
    'submit_order': '/api/investor/{version}/accounts/{investor_id}/orders',
    'loans': '/api/investor/{version}/loans/listing',
    'filters': '/api/investor/{version}/accounts/{investor_id}/filters',
}

INVESTOR_ID_ENV = 'LENDING_CLUB_INVESTOR_ID'

REQUEST_LIMIT_PER_SEC = 1.0


# Interface enums
# pylint: disable=too-few-public-methods
class NoteStatus(Enum):
    """
    Enum of note status
    """
    CHARGED_OFF = 'Charged Off'
    CURRENT = 'Current'
    FULLY_PAID = 'Fully Paid'
    ISSUED = 'Issued'


class ResponseCode(Enum):
    """
    Enum of the Lending Club response code for a request
    """
    SUCCESSFUL = 200
    ERROR = 400
    AUTH_ERROR = 403
    NOT_FOUND_ERROR = 404
    FATAL = 500


class TransferFrequency(Enum):
    """
    Enum for transfer frequency to the account
    """
    NOW = "LOAD_NOW"
    ONCE = "LOAD_ONCE"
    WEEKLY = "LOAD_WEEKLY"
    BIWEEKLY = "LOAD_BIWEEKLY"
    DAY_1_AND_16 = "LOAD_ON_DAY_1_AND_16"
    MONTHLY = "LOAD_MONTHLY"
# pylint: enable=too-few-public-methods
