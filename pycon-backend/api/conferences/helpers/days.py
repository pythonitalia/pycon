import typing
from datetime import date, timedelta


def daterange(start_date: date, end_date: date) -> typing.Iterator[date]:
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(days=n)
