import typing
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.websockets import WebSocket

from association.domain.repositories.association_repository import AssociationRepository


@dataclass
class Context:
    request: typing.Union[Request, WebSocket]
    session: AsyncSession

    @property
    def association_repository(self) -> AssociationRepository:
        return AssociationRepository(session=self.session)


class Info:
    context: Context
