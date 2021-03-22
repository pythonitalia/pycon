# isort: off
import asyncio
import os
import sys  # noqa

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  # noqa

from db_utils import create_database, database_exists

from users.db import get_engine
from users.domain.entities import mapper_registry
from users.settings import DATABASE_URL


async def run():
    engine = get_engine(echo=False)
    metadata = mapper_registry.metadata

    if not database_exists(DATABASE_URL):
        create_database(DATABASE_URL)

        async with engine.begin() as connection:
            await connection.run_sync(metadata.create_all)
    else:
        async with engine.begin() as connection:
            await connection.run_sync(metadata.drop_all)
            await connection.run_sync(metadata.create_all)


if __name__ == "__main__":
    asyncio.run(run())
