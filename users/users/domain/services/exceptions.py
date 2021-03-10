class WrongEmailOrPasswordError(Exception):
    """Raised when we can't find a user with the username/password
    combination"""


class UserIsNotActiveError(Exception):
    """Raised when the user is marked as not active"""


class EmailAlreadyUsedError(Exception):
    """Raised when the email is already used by some other user"""


class UserIsNotAdminError(Exception):
    """Raised when the login is configurated to reject non-admin users"""
