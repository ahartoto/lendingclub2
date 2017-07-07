# Filename: filter.py

"""
LendingClub2 Filter Module
"""

# Standard libraries
from abc import ABC, abstractmethod

# lendingclub2
from lendingclub2.error import LCError


# pylint: disable=too-few-public-methods
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
