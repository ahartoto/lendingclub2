# Filename: loan.py

"""
LendingClub2 Loan Module
"""

# Standard libraries
import json
from operator import attrgetter

# lendingclub2
from lendingclub2 import request
from lendingclub2.config import API_VERSION, DNS, ENDPOINTS
from lendingclub2.error import LCError
from lendingclub2.response import Response


# Constants
LISTING_VERSION = '1.3'


# Interface classes
class Borrower:
    """
    Information of the borrower
    """
    def __init__(self, response):
        """
        Constructor

        :param response: dict
        """
        self._response = response

    def __repr__(self):
        """
        String representation of the borrower

        :returns: string
        """
        return "Borrower(credit_score={}, employed={})".format(
            self.credit_score, self.employed,
        )

    @property
    def address_state(self):
        """
        Get the address state of the loaner

        :returns: string (two characters)
        """
        return self._response['addrState']

    @property
    def credit_score(self):
        """
        Get the credit score of the loaner

        :returns: string
        """
        return "{}-{}".format(self._response['ficoRangeLow'],
                              self._response['ficoRangeHigh'])

    @property
    def delinquency_in_2_years(self):
        """
        The Number of 30+ days past-due incidences of delinquency
        in the borrower's credit file for the past 2 years.

        :returns: integer
        """
        return self._response['delinq2Yrs'] or 0

    @property
    def dti(self):
        """
        Debt-to-income ratio

        :returns: float
        """
        return self._response['dti'] or 0.0

    @property
    def employed(self):
        """
        Check if the borrower is employed

        :returns: boolean
        """
        return self.employment_length >= 0

    @property
    def employment_length(self):
        """
        The length of employment

        :returns: int (-1 if not employed) - number of months being employed
        """
        if self._response['empLength'] is None:
            return -1
        return self._response['empLength']

    @property
    def income_verified(self):
        """
        LC had verified the income of the borrower

        :returns: boolean
        """
        return self._response['isIncV'] == 'VERIFIED'

    @property
    def inquiries_in_last_6_mo(self):
        """
        The Number of inquiries by creditors during the past 6 months.

        :returns: integer
        """
        return self._response['inqLast6Mths'] or 0

    @property
    def months_since_last_delinq(self):
        """
        The Number of months since the borrower's last delinquency.

        :returns: integer
        """
        return self._response['mthsSinceLastDelinq'] or 0

    @property
    def mortgage_accounts(self):
        """
        Number of mortgage accounts.

        :returns: integer
        """
        return self._response['mortAcc'] or 0

    @property
    def public_records(self):
        """
        Number of derogatory public records.

        :returns: integer
        """
        return self._response['pubRec'] or 0

    @property
    def revolving_balance(self):
        """
        Total credit revolving balance.

        :returns: float
        """
        return self._response['revolBal'] or 0.0

    @property
    def title(self):
        """
        Employment title

        :returns: string or None
        """
        return self._response['empTitle']


class Loan:
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
                       self.id, self.amount, self.percent_funded,
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
    def borrower(self):
        """
        Get the information of the borrower

        :returns: instance of lendingclub2.loan.Borrower
        """
        return Borrower(self._response)

    @property
    def expected_default_rate(self):
        """
        The expected default rate of the loan

        :returns: float
        """
        return self._response['expDefaultRate']

    @property
    def description(self):
        """
        Get the description of the loan

        :returns: string or None
        """
        return self._response['desc']

    @property
    def grade(self):
        """
        Get the grade of the loan

        :returns: string
        """
        return self._response['grade']

    @property
    def installment(self):
        """
        Expected monthly payment owed by borrower

        :returns: float
        """
        return self._response['installment']

    @property
    def interest_rate(self):
        """
        Get the interest rate

        :returns: float (0 - 100.0)
        """
        return self._response['inRate']

    @property
    def investor_count(self):
        """
        Get the number of investors already purchased the notes

        :returns: int
        """
        return self._response['investorCount'] or 0

    @property
    def percent_funded(self):
        """
        Find percentage of amount funded

        :returns: float (0 - 100.0)
        """
        return self.funded_amount * 100.0 / self.amount

    @property
    def purpose(self):
        """
        Get the purpose of the loan

        :returns: string
        """
        return self._response['purpose']


class Listing:
    """
    Loan listing, which can be used for filtering, and order submission later
    """
    def __init__(self):
        """
        Constructor
        """
        self.loans = list()

    def __add__(self, other):
        """
        Add two listings together

        :param other: instance of lendingclub2.loan.Listing
        :returns: instance of lendingclub2.loan.Listing
        """
        new_listing = Listing()
        new_listing.loans = list(self.loans) + list(other.loans)
        return new_listing

    def __contains__(self, loan_id):
        """
        Check if the items are in the listing

        :param loan_id: int
        :returns: boolean
        """
        for loan in self.loans:
            if loan.id == loan_id:
                return True
        return False

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

    def __getitem__(self, loan_id):
        """
        Get the loan instance based on the ID

        :param loan_id: int - loan ID
        :raises IndexError: if the loan ID is not in the listing
        :returns: instance of lendingclub2.loan.Loan
        """
        for loan in self.loans:
            if loan.id == loan_id:
                return loan
        raise IndexError("loan with ID {} is not in listing".format(loan_id))

    def __iter__(self):
        """
        Get an iterable version of the listing

        :returns: an iterable
        """
        return iter(self.loans)

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
        response = Response(request.get(url, headers=headers))
        if not response.successful:
            fstr = "cannot search for any loans"
            raise LCError(fstr, details=json.dumps(response.json, indent=2))

        # Reset the stored loans whenever we search again as long as the
        # latest request was successful
        self.loans = list()
        try:
            for loan_json in response.json['loans']:
                loan = Loan(loan_json)
                self.loans.append(loan)
        except KeyError:
            pass

    def sort(self, by_grade=True, by_term=False):
        """
        Sort the listing

        :param by_grade: boolean
        :param by_term: boolean
        """
        if not self.loans:
            return

        if by_grade:
            self.loans = sorted(self.loans, key=attrgetter('grade',
                                                           'subgrade', 'id'))
        elif by_term:
            self.loans = sorted(self.loans, key=attrgetter('term', 'id'))
        else:
            self.loans = sorted(self.loans, key=attrgetter('percent_funded'),
                                reverse=True)
