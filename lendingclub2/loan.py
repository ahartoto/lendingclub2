# Filename: loan.py

"""
LendingClub2 Loan Module
"""

# Standard libraries
import json

# lendingclub2
from lendingclub2 import requests
from lendingclub2.config import API_VERSION, DNS, ENDPOINTS
from lendingclub2.error import LCError
from lendingclub2.response import Response


# Constants
LISTING_VERSION = '1.2'


# Interface classes
class Loan(object):
    """
    Information of each loan
    """
    def __init__(self, response):
        """
        Constructor

        :param response: dict
        """
        self._response = response

        self.id = response['id']
        self.amount = response['loanAmount']
        self.funded_amount = response['fundedAmount']
        self.term = response['term']
        self.subgrade = response['subGrade']

    def __repr__(self):
        """
        Get the string representation of a loan

        :returns: string
        """
        template = "Loan(id={}, amount={:.2f}, funded={:.2f}%, term={}," \
                   " grade={})".format(
                       self.id, self.amount, self.percent_funded * 100,
                       self.term, self.subgrade)
        return template

    @property
    def approved(self):
        """
        Check if the loan has been approved by LendingClub

        :returns: boolean
        """
        return self._response['reviewStatus'] == 'APPROVED'

    @property
    def grade(self):
        """
        Get the grade of the loan

        :returns: string
        """
        return self._response['grade']

    @property
    def percent_funded(self):
        """
        Find percentage of amount funded

        :returns: float
        """
        return self.funded_amount / self.amount


class Listing(object):
    """
    Loan listing, which can be used for filtering, and order submission later
    """
    def __init__(self):
        """
        Constructor
        """
        self.loans = list()

    def __copy__(self):
        """
        Shallow copy of the listing

        :returns: instance of lendingclub2.loan.Listing
        """
        new_listing = Listing()
        new_listing.loans = list(self.loans)
        return new_listing

    def __eq__(self, other):
        """
        Check if two listings are equal

        :param other: instance of lendingclub2.loan.Listing
        :returns: boolean
        """
        return self.loans == other.loans

    def __iter__(self):
        """
        Get an iterable version of the listing

        :returns: an iterable
        """
        return self.loans.__iter__()

    def __len__(self):
        """
        Get the length of loans in the listing

        :returns: int
        """
        return len(self.loans)

    def copy(self):
        """
        Get a shallow copy of the listing

        :returns: instance of lendingclub2.loan.Listing
        """
        return self.__copy__()

    def filter(self, *filters):
        """
        Apply all filters to the search that we had found before.
        If multiple filters are specified, the loan has to meet all the
        criteria to be included in the result.

        :param filters: iterable of lendingclub2.filter.Filter
        :returns: an instance of lendingclub2.loan.Listing
        """
        if not filters:
            return self.copy()

        filtered = list()
        for loan in self.loans:
            meet_spec = True
            for filter_spec in filters:
                if not filter_spec.meet_requirement(loan):
                    meet_spec = False
                    break
            if meet_spec:
                filtered.append(loan)
        new_listing = Listing()
        new_listing.loans = filtered
        return new_listing

    def search(self, filter_id=None, show_all=None):
        """
        Apply filters and search for loans matching the specifications
        """
        url = DNS + ENDPOINTS['loans'].format(version=API_VERSION)

        criteria = list()
        if filter_id is not None:
            criteria.append('filterId={}'.format(filter_id))
        if show_all is not None:
            if show_all:
                criteria.append('showAll=true')
            else:
                criteria.append('showAll=false')

        if criteria:
            url += '?' + '&'.join(criteria)

        headers = {'X-LC-LISTING-VERSION': LISTING_VERSION}
        response = Response(requests.get(url, headers=headers))
        if not response.successful:
            fstr = "cannot search for any loans"
            raise LCError(fstr, details=json.dumps(response.json, indent=2))

        # Reset the stored loans whenever we search again as long as the
        # latest request was successful
        self.loans = list()
        for loan_json in response.json['loans']:
            loan = Loan(loan_json)
            self.loans.append(loan)
