import typing
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.websockets import WebSocket
from users.domain.repository import UsersRepository


@dataclass
class Context:
    request: typing.Union[Request, WebSocket]
    session: AsyncSession

    @property
    def users_repository(self) -> UsersRepository:
        return UsersRepository(session=self.session)


class Info:
    context: Context
