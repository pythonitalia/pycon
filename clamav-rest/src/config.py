from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: SecretStr
