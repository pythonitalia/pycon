from sqlalchemy.engine.url import URL, make_url
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL")
JWT_AUTH_SECRET = config("JWT_AUTH_SECRET", cast=Secret)
JWT_EXPIRES_AFTER_IN_MINUTES = config(
    "JWT_EXPIRES_AFTER_IN_MINUTES", cast=int, default=10
)

PASSWORD_HASHERS = [
    "users.starlette_password.hashers.Argon2PasswordHasher",
    "users.starlette_password.hashers.PBKDF2PasswordHasher",
    "users.starlette_password.hashers.PBKDF2SHA1PasswordHasher",
    "users.starlette_password.hashers.BCryptSHA256PasswordHasher",
]

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
