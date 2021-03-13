from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from users.settings import DATABASE_URL


def get_engine(*, echo=True):
    return create_async_engine(DATABASE_URL, echo=echo)


def get_session(engine):
    return AsyncSession(engine)
