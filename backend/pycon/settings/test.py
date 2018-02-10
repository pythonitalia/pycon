from .base import * # noqa


SECRET_KEY = 'this-key-should-only-be-used-for-tests'

# Make sure that we never use live keys when testing
STRIPE_LIVE_PUBLIC_KEY = ''
STRIPE_LIVE_SECRET_KEY = ''
STRIPE_TEST_PUBLIC_KEY = env('STRIPE_TEST_PUBLIC_KEY')
STRIPE_TEST_SECRET_KEY = env('STRIPE_TEST_SECRET_KEY')
STRIPE_LIVE_MODE = False
