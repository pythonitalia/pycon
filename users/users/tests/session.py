import logging
from unittest.mock import patch

from sqlalchemy.ext.asyncio import AsyncSession
from ward import fixture

from users.db import get_engine

logger = logging.getLogger(__name__)
engine = get_engine(echo=False)
test_session = AsyncSession(engine)


@fixture
async def db():
    with patch("main.get_session", return_value=test_session):
        yield None

    await test_session.rollback()
    logger.debug("rolling back after unit-test done")
