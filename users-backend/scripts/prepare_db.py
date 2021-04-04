# isort: off
import asyncio
import os
import sys

from sqlalchemy.engine.url import make_url  # noqa

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  # noqa

from db_utils import create_database, database_exists

from users.db import get_engine
from users.domain.entities import mapper_registry
from users.settings import DATABASE_URL


async def run():
    engine = get_engine(echo=False)
    metadata = mapper_registry.metadata
    db_name = make_url(DATABASE_URL).database
    sync_database_url = DATABASE_URL.replace("asyncpg", "psycopg2").replace("TEST_", "")

    if not database_exists(sync_database_url, db_name):
        create_database(sync_database_url, db_name)

        async with engine.begin() as connection:
            await connection.run_sync(metadata.create_all)
    else:
        async with engine.begin() as connection:
            await connection.run_sync(metadata.drop_all)
            await connection.run_sync(metadata.create_all)


if __name__ == "__main__":
    asyncio.run(run())
