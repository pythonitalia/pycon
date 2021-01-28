from typing import Optional

from sqlalchemy.sql.expression import select
from users.base.domain.repository import BaseSQLAlchemyRepository
from users.domain.entities import User


class AbstractUsersRepository:
    async def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError()

    async def get_by_id(self, id: int) -> Optional[User]:
        raise NotImplementedError()


class UsersRepository(AbstractUsersRepository, BaseSQLAlchemyRepository):
    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        user = (await self.session.execute(query)).scalar_one_or_none()
        return user

    async def get_by_id(self, id: int) -> Optional[User]:
        query = select(User).where(User.id == id)
        user = (await self.session.execute(query)).scalar_one_or_none()
        return user
