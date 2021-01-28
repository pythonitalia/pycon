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
    "starlette_password.hashers.Argon2PasswordHasher",
    "starlette_password.hashers.PBKDF2PasswordHasher",
    "starlette_password.hashers.PBKDF2SHA1PasswordHasher",
    "starlette_password.hashers.BCryptSHA256PasswordHasher",
]

RUNNING_TESTS = config("RUNNING_TESTS", cast=bool, default=False)

if RUNNING_TESTS:
    PASSWORD_HASHERS = ["starlette_password.plain_hasher.PlainPasswordHasher"]
