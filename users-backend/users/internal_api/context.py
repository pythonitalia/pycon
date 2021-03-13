from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from users.domain.repository import UsersRepository


@dataclass
class Info:
    context: Context


@dataclass
class Context:
    request: Request
    session: AsyncSession

    @property
    def users_repository(self) -> UsersRepository:
        return UsersRepository(session=self.session)
