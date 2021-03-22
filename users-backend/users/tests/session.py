import logging
from unittest.mock import patch

from ward import fixture

from users.db import get_engine, get_session
from users.domain.entities import mapper_registry

logger = logging.getLogger(__name__)
engine = get_engine(echo=False)
test_session = get_session(engine)


@fixture
async def db():
    with patch("main.get_session", return_value=test_session):
        yield test_session

    metadata = mapper_registry.metadata

    async with engine.begin() as connection:
        for table in metadata.sorted_tables:
            await connection.execute(table.delete())

    logger.debug("rolling back after unit-test done")


@fixture
async def second_session():
    return get_session(engine)
