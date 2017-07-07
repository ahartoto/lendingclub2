# Filename: filter.py

"""
LendingClub2 Filter Module
"""

# Standard libraries
from abc import ABC, abstractmethod


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
# pylint: enable=too-few-public-methods
