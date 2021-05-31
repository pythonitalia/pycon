import typing
from dataclasses import dataclass

from starlette.requests import Request
from starlette.websockets import WebSocket

from src.association_membership.domain.repository import AssociationMembershipRepository
from src.customers.domain.repository import CustomersRepository


@dataclass
class Context:
    request: typing.Union[Request, WebSocket]

    @property
    def association_repository(self) -> AssociationMembershipRepository:
        return AssociationMembershipRepository()

    @property
    def customers_repository(self) -> CustomersRepository:
        return CustomersRepository()
