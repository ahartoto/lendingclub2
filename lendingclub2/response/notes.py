# Filename: notes.py

"""
LendingClub2 Notes Response Module
"""

# lendingclub2
from lendingclub2 import request
from lendingclub2.config import API_VERSION, DNS, ENDPOINTS, NoteStatus
from lendingclub2.response import Response


class Note:
    """
    Information of a note
    """
    def __init__(self, response):
        """
        Constructor

        :param response: dict
        """
        self._response = response

    def __repr__(self):
        """
        Get the string representation of the note

        :returns: string
        """
        return "Note(id={}, grade={}, amount={:.2f})".format(
            self.id, self.grade, self.amount,
        )

    @property
    def amount(self):
        """
        Get the amount of the note

        :returns: float
        """
        return self._response['noteAmount']

    @property
    def charged_off(self):
        """

        :returns: boolean
        """
        return self.status == NoteStatus.CHARGED_OFF

    @property
    def current(self):
        """
        Check if the payment for the note is current

        :returns: boolean
        """
        return self.status == NoteStatus.CURRENT

    @property
    def id(self):
        """
        Get the id of the note

        :returns: int
        """
        return self._response['noteId']

    @property
    def grade(self):
        """
        Get the grade of the note

        :returns: string
        """
        return self._response['grade']

    @property
    def late(self):
        """
        Check if a note's payment is late

        :returns: boolean
        """
        return not self.new and not self.current and not self.paid and \
            not self.charged_off

    @property
    def loan_amount(self):
        """
        Get the total amount of loan associated with the note

        :returns: float
        """
        return self._response['loanAmount']

    @property
    def loan_id(self):
        """
        Get the loan ID

        :returns: int
        """
        return self._response['loanId']

    @property
    def loan_length(self):
        """
        Get the total loan length in months

        :returns: int
        """
        return self._response['loanLength']

    @property
    def new(self):
        """
        Check if a note is just issued

        :returns: boolean
        """
        return self.status == NoteStatus.ISSUED

    @property
    def paid(self):
        """
        Check if a note is fully paid

        :returns: boolean
        """
        return self.status == NoteStatus.FULLY_PAID

    @property
    def status(self):
        """
        Get the status of the loan

        :returns: string
        """
        return self._response['loanStatus']


class Notes(Response):
    """
    Get the response of detailed_notes endpoint
    """
    def __init__(self, investor_id):
        """
        Constructor

        :param investor_id: int
        """
        self._investor_id = investor_id
        response = request.get(self.url)
        Response.__init__(self, response)
        self._notes = list()
        try:
            self._notes = [Note(note_json)
                           for note_json in self.json['myNotes']]
        except KeyError:
            pass

    def __iter__(self):
        """
        Get the iterable version of notes

        :returns: an iterable
        """
        return iter(self._notes)

    def __len__(self):
        """
        Find the number of notes

        :returns: int
        """
        return len(self._notes)

    @property
    def url(self):
        """
        Find the relevant url

        :returns: string
        """
        url = DNS + ENDPOINTS['detailed_notes'].format(
            version=API_VERSION, investor_id=self._investor_id)
        return url
