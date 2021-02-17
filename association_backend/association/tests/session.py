import logging
from unittest.mock import patch

from association.db import get_engine, get_session
from association.domain.entities.subscription_entities import mapper_registry
from ward import fixture

logger = logging.getLogger(__name__)
engine = get_engine(echo=False)
test_session = get_session(engine)


@fixture
async def db():
    with patch("main.get_session", return_value=test_session):
        yield test_session

    await test_session.rollback()
    logger.debug("rolling back after unit-test done")


@fixture
async def second_session():
    return get_session(engine)


@fixture
async def cleanup_db():
    """
    TODO Investigate if this should maybe be the default,
        instead of using `rollback` :)

    Needed only in tests where you plan on calling
    `.commit()` to make sure the entire DB integration
    works. As we cannot rollback committed changes
    this fixture will truncate all database after executing
    the test it's used in
    """
    yield None

    metadata = mapper_registry.metadata

    async with engine.begin() as connection:
        for table in metadata.sorted_tables:
            await connection.execute(table.delete())
