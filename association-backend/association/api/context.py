import typing
from dataclasses import dataclass

# from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.websockets import WebSocket

from association_membership.domain.repository import AssociationMembershipRepository
from customers.domain.repository import CustomersRepository


@dataclass
class Context:
    request: typing.Union[Request, WebSocket]
    session: typing.Any

    @property
    def association_repository(self) -> AssociationMembershipRepository:
        return AssociationMembershipRepository()

    @property
    def customers_repository(self) -> CustomersRepository:
        return CustomersRepository()


class Info:
    context: Context
