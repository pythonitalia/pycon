import typing
from dataclasses import dataclass

from domain.repository import UsersRepository
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.websockets import WebSocket


@dataclass
class Context:
    request: typing.Union[Request, WebSocket]
    session: AsyncSession

    @property
    def users_repository(self) -> UsersRepository:
        return UsersRepository(session=self.session)


class Info:
    context: Context
