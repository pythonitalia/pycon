from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.dataloader import DataLoader

from users.api.dataloader import users_dataloader
from users.domain.repository import UsersRepository

if TYPE_CHECKING:
    from users.domain.entities import User


@dataclass
class Context:
    request: Union[Request, WebSocket]
    session: AsyncSession
    response: Response
    _authenticated_as: Optional["User"] = None

    @property
    def users_repository(self) -> UsersRepository:
        return UsersRepository(session=self.session)

    @property
    def users_dataloader(self) -> DataLoader:
        return users_dataloader


class Info:
    context: Context
