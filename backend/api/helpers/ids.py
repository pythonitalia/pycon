from typing import Optional

from django.conf import settings
from hashids import Hashids


def get_hashids(salt: Optional[str] = None, min_length: int = 4):
    salt = salt or settings.SECRET_KEY

    return Hashids(
        salt=settings.SECRET_KEY,
        min_length=min_length,
        alphabet="abcdefghijklmnopqrstuvwxyz",
    )


def decode_hashid(hashid: str, salt: Optional[str] = None, min_length: int = 4):
    hashids = get_hashids(salt=salt, min_length=min_length)

    return hashids.decode(hashid)[0]


def encode_hashid(value, salt: Optional[str] = None, min_length: int = 4):
    hashids = get_hashids(salt=salt, min_length=min_length)

    return hashids.encode(value)
