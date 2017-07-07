# Filename: filter.py

"""
LendingClub2 Filter Module
"""

# Standard libraries
from abc import ABC, abstractmethod


class Filter(ABC):
    """
    Abstract base class for filtering the loan
    """
    # pylint: disable=too-few-public-methods
    @abstractmethod
    def meet_requirement(self, loan):
        """
        Check if the loan is meeting the filter requirement

        :param loan: instance of lendingclub2.loan.Loan
        :returns: boolean
        """
        return True
    # pylint: enable=too-few-public-methods
