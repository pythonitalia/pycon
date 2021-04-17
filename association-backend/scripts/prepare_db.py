# isort: off
# flake8: noqa
import asyncio
import os
import sys  # noqa

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  # noqa

import sqlalchemy
from db_utils import create_database, database_exists  # noqa

from database.db import metadata
from association.settings import DATABASE_URL


async def run():
    engine = sqlalchemy.create_engine(DATABASE_URL)

    if not database_exists(DATABASE_URL):
        create_database(DATABASE_URL)

        metadata.create_all(engine)
    else:
        metadata.drop_all(engine)
        metadata.create_all(engine)


if __name__ == "__main__":
    asyncio.run(run())
