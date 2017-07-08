# Filename: order.py

"""
LendingClub2 Response Order Module
"""

# lendingclub2
from lendingclub2 import requests
from lendingclub2.config import API_VERSION, DNS, ENDPOINTS
from lendingclub2.error import LCError
from lendingclub2.response import Response
from lendingclub2.response.notes import Note


class OrderNote(object):
    """
    Class to wrap around note to be ordered
    """
    def __init__(self, note, amount, portfolio_id=None):
        """
        Constructor

        :param note: instance of lendingclub2.response.notes.Note
        :param amount: float - must be greater than 0 (usually 25)
        :param portfolio_id: int - portfolio ID which the note will be
                             assigned to if the order is submitted successfully
        """
        if not isinstance(note, Note):
            fstr = "note should be an instance of " \
                   "lendingclub2.response.notes.Note"
            raise LCError(fstr)

        if amount <= 0:
            fstr = "amount should be a positive number"
            raise LCError(fstr)

        self._note = note
        self._amount = amount
        self._portfolio_id = portfolio_id

    @property
    def amount(self):
        """
        Get the amount user wants to buy the note for

        :returns: float
        """
        return self._amount

    @property
    def loan_id(self):
        """
        Get the loan ID of the note user would purchase

        :returns: int
        """
        return self._note.loan_id

    @property
    def portfolio_id(self):
        """
        Get the portfolio ID to assign the note to if the order was successful

        :returns: int or None
        """
        return self._portfolio_id


class Order(Response):
    """
    Submit an order
    """
    def __init__(self, investor_id, *order_notes):
        """
        Constructor

        :param investor_id: int
        """
        self._investor_id = investor_id
        self._order_notes = order_notes

        orders = list()
        for order_note in self._order_notes:
            order = {
                'loanId': order_note.loan_id,
                'requestedAmount': order_note.amount,
            }
            if order_note.portfolio_id is not None:
                order['portfolioId'] = order_note.portfolio_id
            orders.append(order)

        payload = {
            'aid': investor_id,
            'orders': orders,
        }
        response = requests.post(self.url, json=payload)
        Response.__init__(self, response)

    @property
    def url(self):
        """
        Get the relevant URL

        :returns: string
        """
        url = DNS + ENDPOINTS['submit_order'].format(
            version=API_VERSION, investor_id=self._investor_id)
        return url
