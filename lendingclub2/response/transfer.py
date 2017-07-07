# Filename: transfer.py

"""
LendingClub2 Transfer Response Module
"""

# Standard libraries
import datetime

# lendingclub2
from lendingclub2 import requests
from lendingclub2.config import API_VERSION, DNS, ENDPOINTS, TransferFrequency
from lendingclub2.error import LCError
from lendingclub2.response import Response


def add(investor_id, amount, frequency=TransferFrequency.NOW,
        start_date=None, end_date=None):
    """
    Withdraw the account

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
        elif not isinstance(start_date, datetime.datetime):
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

    return Response(requests.post(url, json=payload))


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
    return Response(requests.post(url, json=payload))


def pending(investor_id):
    """
    Retrieve the pending transfers

    :param investor_id: int - the investor account id
    :returns: instance of lendingclub2.response.Response
    """
    url = DNS + ENDPOINTS['pending_transfer'].format(
        version=API_VERSION, investor_id=investor_id)
    return Response(requests.get(url))


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
    return Response(requests.post(url, json=payload))
