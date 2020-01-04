from django.conf import settings
from hashids import Hashids


def get_hashids():
    return Hashids(
        salt=settings.SECRET_KEY, min_length=4, alphabet="abcdefghijklmnopqrstuvwxyz"
    )


def decode_hashid(hashid):
    hashids = get_hashids()

    return hashids.decode(hashid)[0]


def encode_hashid(value):
    hashids = get_hashids()

    return hashids.encode(value)
