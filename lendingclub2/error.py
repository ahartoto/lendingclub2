# Filename: error.py

"""
LendingClub2 Error Module
"""


class LCError(Exception):
    """
    Base exception for lendingclub2 package
    """
    def __init__(self, message, hint=None, details=None, code=1):
        """
        Constructor

        :param message: string
        :param hint: string - hint (default: None)
        :param details: string - details of the exception (default: None)
        :param code: int - error code (default: 1)
        """
        Exception.__init__(self, message)
        self.message = message
        self.hint = hint
        self.details = details
        self.code = code

    def __repr__(self):
        """
        String representation of the instance

        :returns: string
        """
        return "LCError(message: {})".format(self.message)

    def __str__(self):
        """
        Stringify the instance

        :returns: string
        """
        message = [self.message]
        if self.hint is not None:
            message.append("[=== Hint ===]")
            message.append(self.hint)
        if self.details is not None:
            message.append("[=== Details ===]")
            message.append(self.details)
        return "\n".join(message)
