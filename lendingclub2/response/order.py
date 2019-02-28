# Filename: order.py

"""
LendingClub2 Response Order Module
"""

# lendingclub2
from lendingclub2 import request
from lendingclub2.config import API_VERSION, DNS, ENDPOINTS
from lendingclub2.error import LCError
from lendingclub2.response import Response


class OrderNote:
    """
    Class to wrap around note to be ordered
    """
    def __init__(self, loan_id, amount, portfolio_id=None):
        """
        Constructor

        :param loan_id: int
        :param amount: float - must be greater than 0 (usually 25)
        :param portfolio_id: int - portfolio ID which the note will be
                             assigned to if the order is submitted successfully
        """
        if amount <= 0:
            fstr = "amount should be a positive number"
            raise LCError(fstr)
        if amount % 25 != 0:
            fstr = "amount needs to be a multiple of $25"
            raise LCError(fstr)

        self._loan_id = loan_id
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
        return self._loan_id

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
        response = request.post(self.url, json=payload)
        Response.__init__(self, response)

    @property
    def id(self):
        """
        Get the id of the order

        :returns: int
        """
        return self._response.json['orderInstructId']

    @property
    def url(self):
        """
        Get the relevant URL

        :returns: string
        """
        url = DNS + ENDPOINTS['submit_order'].format(
            version=API_VERSION, investor_id=self._investor_id)
        return url

    @property
    def successful(self):
        """
        Determine if the order submission was successful

        :returns: boolean
        """
        if not Response.successful:
            return False

        # Get the confirmation
        for confirm_json in self.json['orderConfirmations']:
            loan_id = confirm_json['loanId']
            note = None
            for order_note in self._order_notes:
                if loan_id == order_note.loan_id:
                    note = order_note
                    break
            if note is None:
                return False

            # Now check if we see ORDER_FULFILLED in executionStatus
            if 'ORDER_FULFILLED' not in confirm_json['executionStatus']:
                return False
            # Now check if the amount is non-zero
            if not confirm_json['investedAmount']:
                return False
        return True
