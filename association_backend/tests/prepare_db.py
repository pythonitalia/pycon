# isort: off
import asyncio
import os
import sys  # noqa

from association.db import get_engine
from association.domain.entities.subscription_entities import mapper_registry
from association.settings import DATABASE_URL
from db_utils import create_database, database_exists

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  # noqa


async def run():
    engine = get_engine(echo=False)
    metadata = mapper_registry.metadata
    if not database_exists(DATABASE_URL):
        create_database(DATABASE_URL)

        async with engine.begin() as connection:
            await connection.run_sync(mapper_registry.metadata.create_all)
    else:
        async with engine.begin() as connection:
            for table in metadata.sorted_tables:
                await connection.execute(table.delete())


if __name__ == "__main__":
    asyncio.run(run())
