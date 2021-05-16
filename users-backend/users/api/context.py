from dataclasses import dataclass
from typing import Optional, Union

from pythonit_toolkit.pastaporto.actions import PastaportoAction
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry.dataloader import DataLoader

from users.api.dataloader import users_dataloader
from users.domain.repository import UsersRepository


@dataclass
class Context:
    request: Union[Request, WebSocket]
    session: AsyncSession
    pastaporto_action: Optional[PastaportoAction] = None

    @property
    def users_repository(self) -> UsersRepository:
        return UsersRepository(session=self.session)

    @property
    def users_dataloader(self) -> DataLoader:
        return users_dataloader


class Info:
    context: Context
