from .base import * # noqa


SECRET_KEY = 'this-key-should-only-be-used-for-tests'

STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
