# Filename: config.py

"""
LendingClub2 Config Module

Interface enums:
    ResponseCode
    TransferFrequency
"""

# Standard libraries
from enum import Enum


# Constants
DNS = 'https://api.lendingclub.com'

ENDPOINTS = {
    'summary': '/api/investor/{version}/accounts/{investor_id}/summary',
    'available_cash': '/api/investor/{version}/accounts'
                      '/{investor_id}/availablecash',
    'transfer': '/api/investor/{version}/accounts'
                '/{investor_id}/funds/add',
    'pending_transfer': '/api/investor/{version}/accounts'
                        '/{investor_id}/funds/pending',
    'cancel_transfer': '/api/investor/{version}/accounts'
                       '/{investor_id}/funds/cancel',
    'notes': '/api/investor/{version}/accounts/{investor_id}/notes',
    'detailed_notes': '/api/investor/{version}/accounts/'
                      '{investor_id}/detailednotes',
    'portfolios': '/api/investor/{version}/accounts/{investor_id}/portfolios',
    'submit_order': '/api/investor/{version}/accounts/{investor_id}/orders',
    'filters': '/api/investor/{version}/accounts/{investor_id}/filters',
}

REQUEST_LIMIT_PER_SEC = 1


# Interface enums
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
    MONTHLY = "LOAD_MONTHLY"
