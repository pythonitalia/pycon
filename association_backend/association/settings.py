from sqlalchemy.engine.url import URL, make_url
from starlette.config import Config

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL")
STRIPE_SUBSCRIPTION_API_SECRET = config("STRIPE_SUBSCRIPTION_API_SECRET", cast=str)
STRIPE_SUBSCRIPTION_API_KEY = config("STRIPE_SUBSCRIPTION_API_KEY", cast=str)
STRIPE_SUBSCRIPTION_PRODUCT_ID = config("STRIPE_SUBSCRIPTION_PRODUCT_ID", cast=str)
STRIPE_SUBSCRIPTION_PRICE_ID = config("STRIPE_SUBSCRIPTION_PRICE_ID", cast=str)
STRIPE_WEBHOOK_SIGNATURE_SECRET = config("STRIPE_WEBHOOK_SIGNATURE_SECRET", cast=str)

STRIPE_SUBSCRIPTION_SUCCESS_URL = config(
    "STRIPE_SUBSCRIPTION_SUCCESS_URL",
    cast=str,
    default="https://association.python.it/payments/success",
)
STRIPE_SUBSCRIPTION_CANCEL_URL = config(
    "STRIPE_SUBSCRIPTION_CANCEL_URL",
    cast=str,
    default="https://association.python.it/payments/cancel",
)

TEST_USER_ID = config("TEST_USER_ID", cast=str, default=101010)
TEST_USER_EMAIL = config("TEST_USER_EMAIL", cast=str, default="user101010@pycon.it")

PASTAPORTO_SECRET = config("PASTAPORTO_SECRET", cast=str)

DOMAIN_URL = config.get("DOMAIN_URL")
RUNNING_TESTS = config("RUNNING_TESTS", cast=bool, default=False)

if RUNNING_TESTS:
    original_url = make_url(DATABASE_URL)
    test_db_url = URL.create(
        drivername=original_url.drivername,
        username=original_url.username,
        password=original_url.password,
        host=original_url.host,
        port=original_url.port,
        database=f"TEST_{original_url.database}",
        query=original_url.query,
    )
    DATABASE_URL = test_db_url
