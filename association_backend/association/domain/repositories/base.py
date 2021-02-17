from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractTransaction:
    session: Any

    def with_session(self, session):
        self.session = session

    def transaction(self):
        raise NotImplementedError()

    async def commit(self):
        raise NotImplementedError()

    async def rollback(self):
        raise NotImplementedError()


class AbstractRepository(AbstractTransaction):
    session: Optional[AsyncSession]

    def __init__(self, session: Optional[AsyncSession] = None) -> None:
        self.session = session

    def transaction(self):
        return self.session.begin()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
