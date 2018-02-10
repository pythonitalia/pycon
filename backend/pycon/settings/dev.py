from .base import * # noqa

DEBUG = True

SECRET_KEY = 'do not use this in production'

# Make sure that we never use live keys on dev
STRIPE_LIVE_PUBLIC_KEY = ''
STRIPE_LIVE_SECRET_KEY = ''
STRIPE_TEST_PUBLIC_KEY = env('STRIPE_TEST_PUBLIC_KEY', default='')
STRIPE_TEST_SECRET_KEY = env('STRIPE_TEST_SECRET_KEY', default='')
STRIPE_LIVE_MODE = False
