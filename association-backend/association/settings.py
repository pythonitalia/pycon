import stripe
from starlette.config import Config

config = Config(".env")

DATABASE_URL = config("DATABASE_URL")
STRIPE_API_KEY = config("STRIPE_API_KEY")
STRIPE_WEBHOOK_SECRET = config("STRIPE_WEBHOOK_SECRET")
SUBSCRIPTION_PRICE_ID = config("STRIPE_PYTHON_ITALIA_SUBSCRIPTION_PRICE_ID")


stripe.api_key = STRIPE_API_KEY
