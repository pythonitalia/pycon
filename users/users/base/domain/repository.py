from sqlalchemy.ext.asyncio import AsyncSession


class BaseSQLAlchemyRepository:
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def transaction(self):
        return self.session.begin()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
