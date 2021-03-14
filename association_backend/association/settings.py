from sqlalchemy.engine.url import URL, make_url
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL")
JWT_USERS_PRIVATE_KEY = config("JWT_USERS_PRIVATE_KEY", cast=Secret)
JWT_USERS_PUBLIC_KEY = config("JWT_USERS_PUBLIC_KEY", cast=Secret)
JWT_USERS_VERIFY_SIGNATURE = config(
    "JWT_USERS_VERIFY_SIGNATURE", cast=bool, default=True
)
JWT_USERS_COOKIE_NAME = config("JWT_USERS_COOKIE_NAME", cast=str, default="pycon_jwt")
JWT_USERS_JWT_EXPIRES_AFTER_IN_MINUTES = config(
    "JWT_USERS_JWT_EXPIRES_AFTER_IN_MINUTES", cast=int, default=10
)
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
PASTAPORTO_ACTION_X_HEADER = config("PASTAPORTO_ACTION_X_HEADER", cast=str)
PASTAPORTO_ACTION_SECRET = config("PASTAPORTO_ACTION_SECRET", cast=str)

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
