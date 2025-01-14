from contextlib import contextmanager
from django.db import connection


@contextmanager
def set_seed(seed: int):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT setseed({seed})")
        yield
        cursor.execute("SELECT setseed(0)")
