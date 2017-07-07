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
        self.review_status = response['reviewStatus']

    def __repr__(self):
        """
        Get the string representation of a loan

        :returns: string
        """
        template = "Loan(id={}, amount={}, funded={:.2f}%, term={}," \
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
        return self.review_status == 'APPROVED'

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

    def filter(self, *filters):
        """
        Apply filters to the search that we had found before

        :param filters: iterable of lendingclub2.filter.Filter
        :returns: an iterable of lendingclub2.loan.Loan
        """
        if not filters:
            return list(self.loans)

        filtered = list()
        for loan in self.loans:
            for filter_spec in filters:
                lc_filter = filter_spec()
                if lc_filter.meet_requirement(loan):
                    filtered.append(loan)
                    break
        return filtered

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
