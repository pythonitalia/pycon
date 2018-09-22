from .base import *  # noqa


SECRET_KEY = 'this-key-should-only-be-used-for-tests'


API_SETTINGS = {
    'PAGINATION': {
        'LIMIT_MAX_VALUE': 50,
        'LIMIT_MIN_VALUE': 1,
        'LIMIT_DEFAULT_VALUE': 10,
    }
}
