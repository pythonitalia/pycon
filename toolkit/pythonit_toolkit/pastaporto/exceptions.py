class InvalidPastaportoError(Exception):
    """Raised when the pastaporto received from the gateway
    is not valid such as: expired, invalid signature and so on"""
