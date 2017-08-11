# Filename: request.py

"""
LendingClub2 Request Module

Interface functions:
    get
    post
"""

# Standard libraries
import datetime
import time

# Requests
import requests

# Lending Club
from lendingclub2.authorization import Authorization
from lendingclub2.config import REQUEST_LIMIT_PER_SEC
from lendingclub2.error import LCError

__LAST_REQUEST_TIMESTAMP = None


# pylint: disable=global-statement
def get(*args, **kwargs):
    """
    Wrapper around requests.get function.

    :param args: tuple - positional arguments for requests.get
    :param kwargs: dict - keyword arguments for requests.get
    :returns: instance of requests.Response
    """
    global __LAST_REQUEST_TIMESTAMP
    __add_headers_to_kwargs(kwargs)
    __wait_request()
    try:
        response = requests.get(*args, **kwargs)
        __LAST_REQUEST_TIMESTAMP = datetime.datetime.now()
        return response
    except requests.ConnectionError as exc:
        fstr = "Cannot connect correctly"
        raise LCError(fstr, details=str(exc))
# pylint: enable=global-statement


# pylint: disable=global-statement
def post(*args, **kwargs):
    """
    Wrapper around requests.post function.

    :param args: tuple - positional arguments for requests.post
    :param kwargs: dict - keyword arguments for requests.post
    :returns: instance of requests.Response
    """
    global __LAST_REQUEST_TIMESTAMP
    __add_headers_to_kwargs(kwargs)
    __wait_request()
    try:
        response = requests.post(*args, **kwargs)
        __LAST_REQUEST_TIMESTAMP = datetime.datetime.now()
        return response
    except requests.ConnectionError as exc:
        fstr = "Cannot connect correctly"
        raise LCError(fstr, details=str(exc))
# pylint: enable=global-statement


# Internal functions
def __add_headers_to_kwargs(kwargs):
    """
    Add authorization key to the headers in keyword arguments

    :param kwargs: dict
    """
    auth = Authorization()
    if 'headers' in kwargs:
        for key, value in auth.header.items():
            kwargs['headers'][key] = value
    else:
        kwargs['headers'] = auth.header


def __wait_request():
    """
    Ensure that we are not violating the requirements on sending request
    at the correct rate
    """
    if __LAST_REQUEST_TIMESTAMP is None:
        return

    now = datetime.datetime.now()
    delta = now - __LAST_REQUEST_TIMESTAMP
    total_seconds = delta.total_seconds()
    wait_time_between_requests = 1.0 / REQUEST_LIMIT_PER_SEC
    if total_seconds < wait_time_between_requests:
        wait_time = wait_time_between_requests - total_seconds
        time.sleep(wait_time)
