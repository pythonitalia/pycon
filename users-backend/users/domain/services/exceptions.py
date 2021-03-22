class WrongEmailOrPasswordError(Exception):
    """Raised when we can't find a user with the username/password
    combination"""


class UserIsNotActiveError(Exception):
    """Raised when the user is marked as not active"""


class EmailAlreadyUsedError(Exception):
    """Raised when the email is already used by some other user"""


class UserIsNotAdminError(Exception):
    """Raised when the login is configured to reject non-admin users"""


class ResetPasswordTokenInvalidError(Exception):
    """Raised when the reset password token JWT-ID is not valid anymore"""


class ResetPasswordTokenExpiredError(Exception):
    """Raised when the reset password token is expired"""


class UserDoesNotExistError(Exception):
    """Raised when the user requested does not exist"""
