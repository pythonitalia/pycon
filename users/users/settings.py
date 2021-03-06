from sqlalchemy.engine.url import URL, make_url
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL")
SESSION_SECRET_KEY = config("SESSION_SECRET_KEY", cast=Secret)

# Google social auth
GOOGLE_AUTH_CLIENT_ID = config("GOOGLE_AUTH_CLIENT_ID", cast=Secret, default=None)
GOOGLE_AUTH_CLIENT_SECRET = config(
    "GOOGLE_AUTH_CLIENT_SECRET", cast=Secret, default=None
)

SOCIAL_LOGIN_JWT_COOKIE_NAME = config(
    "SOCIAL_LOGIN_JWT_COOKIE_NAME", cast=str, default="social-jwt-token"
)

# Identity / Pastaporto secrets
IDENTITY_SECRET = config("IDENTITY_SECRET", cast=Secret)
PASTAPORTO_SECRET = config("PASTAPORTO_SECRET", cast=Secret)
SERVICE_TO_SERVICE_SECRET = config(
    "SERVICE_TO_SERVICE_SECRET", cast=Secret, default=None
)

IDENTITY_EXPIRES_AFTER_MINUTES = config(
    "IDENTITY_EXPIRES_AFTER_MINUTES", cast=int, default=60
)

# Pagination

DEFAULT_PAGINATION_TO = 20

# Headers config

SERVICE_KEY_X_HEADER = "x-service-key"

# Passwords

PASSWORD_HASHERS = [
    "users.starlette_password.hashers.Argon2PasswordHasher",
    "users.starlette_password.hashers.PBKDF2PasswordHasher",
    "users.starlette_password.hashers.PBKDF2SHA1PasswordHasher",
    "users.starlette_password.hashers.BCryptSHA256PasswordHasher",
]

# Unit test configuration

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
    PASSWORD_HASHERS = ["users.starlette_password.plain_hasher.PlainPasswordHasher"]
    SERVICE_TO_SERVICE_SECRET = "test-service-to-service"
