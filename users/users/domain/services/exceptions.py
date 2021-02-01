class UsernameOrPasswordInvalidError(Exception):
    pass


class UserIsNotActiveError(Exception):
    pass


class EmailAlreadyUsedError(Exception):
    """Raised when the email is already used by some other user"""
