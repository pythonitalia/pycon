class ResetPasswordTokenNotValidError(Exception):
    """
    Raised when the token passed to reset user's password
    is not valid
    """


class UserDoesNotExistError(Exception):
    """
    Raised when no user with the ID used can be found
    """
