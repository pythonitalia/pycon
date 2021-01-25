from sqlalchemy.ext.asyncio import AsyncSession


class BaseSQLAlchemyRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        return self._session
