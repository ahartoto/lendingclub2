# Filename: filter.py

"""
LendingClub2 Filter Module
"""

# Standard libraries
import collections
from abc import abstractmethod

try:
    from abc import ABC
except ImportError:
    # Support for Python version older than 3.4
    # pylint: disable=unused-import
    from abc import ABCMeta
    # pylint: enable=unused-import

    # pylint: disable=too-few-public-methods
    class ABC(metaclass=ABCMeta):
        """
        Helper class that has ABCMeta as its metaclass.
        """
        pass
    # pylint: enable=too-few-public-methods


# lendingclub2
from lendingclub2.error import LCError


# pylint: disable=too-few-public-methods
class BorrowerTrait(ABC):
    """
    Abstract base class to define borrowers of interest
    """
    @abstractmethod
    def matches(self, borrower):
        """
        Check if borrower has the trait

        :param borrower: instance of lendingclub2.loan.Borrower
        :returns: boolean
        """
        return True


class BorrowerEmployedTrait(BorrowerTrait):
    """
    Check if borrower is employed
    """
    def matches(self, borrower):
        """
        Check if borrower has the trait

        :param borrower: instance of lendingclub2.loan.Borrower
        :returns: boolean
        """
        return borrower.employed


class Filter(ABC):
    """
    Abstract base class for filtering the loan
    """
    @abstractmethod
    def meet_requirement(self, loan):
        """
        Check if the loan is meeting the filter requirement

        :param loan: instance of lendingclub2.loan.Loan
        :returns: boolean
        """
        return True


class FilterByApproved(Filter):
    """
    Filter by if the loan is already approved
    """
    def meet_requirement(self, loan):
        """
        Check if the loan is meeting the filter requirement

        :param loan: instance of lendingclub2.loan.Loan
        :returns: boolean
        """
        return loan.approved


class FilterByBorrowerTraits(Filter):
    """
    Filter to have borrower matching specific traits
    """
    def __init__(self, traits):
        """
        Constructor

        :param traits: instance of lendingclub2.filter.BorrowerTrait
                       or iterable of instance of
                       lendingclub2.filter.BorrowerTrait
        """
        if isinstance(traits, collections.Iterable):
            self._specs = traits
        elif isinstance(traits, BorrowerTrait):
            self._specs = (traits, )
        else:
            fstr = "invalid traits type for {}".format(self.__class__.__name__)
            raise LCError(fstr)

    def meet_requirement(self, loan):
        """
        Check if the loan is meeting the filter requirement

        :param loan: instance of lendingclub2.loan.Loan
        :returns: boolean
        """
        for spec in self._specs:
            if not spec.matches(loan.borrower):
                return False
        return True


class FilterByFunded(Filter):
    """
    Filter by percentage funded
    """
    def __init__(self, percentage):
        """
        Constructor.

        :param percentage: float (between 0 and 100 inclusive)
        """
        if percentage < 0.0 or percentage > 100.0:
            fstr = "percentage needs to be between 0 and 100 (inclusive)"
            raise LCError(fstr)

        self._percentage = percentage

    def meet_requirement(self, loan):
        """
        The loan would have to be at least the percentage value to meet the
        requirement.

        :param loan: instance of lendingclub2.loan.Loan
        :returns: boolean
        """
        return loan.percent_funded >= self._percentage


class FilterByGrade(Filter):
    """
    Filter by grade
    """
    def __init__(self, grades=None):
        """
        Constructor

        :param grades: iterable of string (default: None, example: ('A', 'B'))
        """
        self._grades = grades

    def meet_requirement(self, loan):
        """
        Check if the loan is meeting the filter requirement

        :param loan: instance of lendingclub2.loan.Loan
        :returns: boolean
        """
        if self._grades and loan.grade in self._grades:
            return True
        return False


class FilterByTerm(Filter):
    """
    Filter by term
    """
    def __init__(self, value=36, min_val=None, max_val=None):
        """
        Constructor. To filter by a specific value, set value to a number.
        To filter by a range, set value to None, and set min_val and max_val
        to integers.

        :param value: int - exact term value (default: 36)
        :param min_val: int - minimum term value (inclusive) (default: None)
        :param max_val: int - maximum term value (inclusive) (default: None)
        """
        if value is not None and (min_val is not None or max_val is not None):
            fstr = "value and min_val, max_val are mutually exclusive"
            details = "value: {}".format(value)
            if min_val is not None:
                details += ", min_val: {}".format(min_val)
            if max_val is not None:
                details += ", max_val: {}".format(max_val)
            raise LCError(fstr, details=details)

        if min_val is not None and max_val is not None:
            if max_val > min_val:
                fstr = "max_val cannot be greater than min_val"
                raise LCError(fstr)
        elif value is None and (min_val is None or max_val is None):
            fstr = "invalid specification on the values"
            hint = "either value or min_val + max_val combo should be specified"
            raise LCError(fstr, hint=hint)

        self._value = value
        self._min_value = min_val
        self._max_value = max_val

    def meet_requirement(self, loan):
        """
        Check if the loan is meeting the filter requirement

        :param loan: instance of lendingclub2.loan.Loan
        :returns: boolean
        """
        if self._value is not None:
            return loan.term == self._value
        return self._min_value <= loan.term <= self._max_value
# pylint: enable=too-few-public-methods
