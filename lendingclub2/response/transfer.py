# Filename: transfer.py

"""
LendingClub2 Transfer Response Module
"""

# Standard libraries
import datetime
import json

# lendingclub2
from lendingclub2 import request
from lendingclub2.config import API_VERSION, DNS, ENDPOINTS, TransferFrequency
from lendingclub2.error import LCError
from lendingclub2.response import Response


# Interface functions
def add(investor_id, amount, frequency=TransferFrequency.NOW,
        start_date=None, end_date=None):
    """
    Add fund to the account

    :param investor_id: int - the investor account id
    :param amount: float - amount to withdraw
    :param frequency: member of lendingclub2.config.TransferFrequency
                      (default: TransferFrequency.NOW)
    :param start_date: instance of datetime.datetime - required if frequency
                       is not TransferFrequency.NOW (default: None)
    :param end_date: instance of datetime.datetime - optional (default: None)
    :returns: instance of lendingclub2.response.Response
    """
    url = DNS + ENDPOINTS['transfer'].format(version=API_VERSION,
                                             investor_id=investor_id)
    if not isinstance(frequency, TransferFrequency):
        fstr = "frequency parameter is not instance of TransferFrequency"
        raise LCError(fstr)

    if frequency != TransferFrequency.NOW:
        if start_date is None:
            fstr = "please specify start_date to transfer fund"
            hint = "start_date needs to be specified for future or recurring " \
                   "transfer"
            raise LCError(fstr, hint=hint)
        if not isinstance(start_date, datetime.datetime):
            fstr = "start_date parameter needs to be an instance of datetime"
            raise LCError(fstr)

    if end_date is not None and not isinstance(end_date, datetime.datetime):
        fstr = "end_date parameter needs to be an instance of datetime"
        raise LCError(fstr)

    if amount <= 0.0:
        fstr = "amount has to be a positive number for transfer"
        raise LCError(fstr)

    payload = {
        'transferFrequency': frequency.value,
        'amount': amount,
    }
    if start_date is not None:
        payload['startDate'] = start_date.isoformat()
    if end_date is not None:
        payload['endDate'] = end_date.isoformat()

    return Response(request.post(url, json=payload))


def cancel(investor_id, *transaction_ids):
    """
    Cancel the pending transactions

    :param investor_id: int - the investor account id
    :param transaction_ids: iterable of int
    :returns: instance of lendingclub2.response.Response if successful,
              None if nothing to cancel
    """
    if not transaction_ids:
        return None

    url = DNS + ENDPOINTS['cancel_transfer'].format(
        version=API_VERSION, investor_id=investor_id)

    payload = {'transferIds': list(transaction_ids)}
    return Response(request.post(url, json=payload))


def pending(investor_id):
    """
    Retrieve the pending transfers

    :param investor_id: int - the investor account id
    :returns: iterable of instance of lendingclub2.response.transfer.Transaction
    """
    url = DNS + ENDPOINTS['pending_transfer'].format(
        version=API_VERSION, investor_id=investor_id)

    response = Response(request.get(url))
    if not response.successful:
        fstr = "cannot find list of pending transactions"
        raise LCError(fstr, details=json.dumps(response.json, indent=2))

    transactions = list()
    total_transactions = 0
    try:
        total_transactions = response.json['transfers']
    except KeyError:
        pass

    for key in range(total_transactions):
        transactions.append(Transaction(response.json[key]))
    return transactions


def withdraw(investor_id, amount):
    """
    Withdraw the account

    :param investor_id: int - the investor account id
    :param amount: float - amount to withdraw
    :returns: instance of lendingclub2.response.Response
    """
    url = DNS + ENDPOINTS['withdraw'].format(version=API_VERSION,
                                             investor_id=investor_id)

    if amount <= 0.0:
        fstr = "amount has to be a positive number for withdrawal"
        raise LCError(fstr)

    payload = {'amount': amount}
    return Response(request.post(url, json=payload))


# Interface classes
class Transaction:
    """
    Transfer transaction
    """
    def __init__(self, response):
        """
        Constructor

        :param response: dict
        """
        self._response = response

    @property
    def amount(self):
        """
        Get the amount in the transaction

        :returns: float
        """
        return self._response['amount']

    @property
    def id(self):
        """
        Get the ID of the transaction. If the response doesn't include
        any ID, the return value is None.

        :returns: int or None
        """
        if 'transactionId' in self._response:
            return self._response['transactionId']
        return None
