from __future__ import annotations

import strawberry

from users.domain import entities
from users.domain.repository import UsersRepository


@strawberry.federation.type(keys=["id"])
class User:
    id: strawberry.ID
    email: str
    fullname: str
    name: str

    @classmethod
    def from_domain(cls, entity: entities.User) -> User:
        return cls(
            id=entity.id, email=entity.email, fullname=entity.fullname, name=entity.name
        )


@strawberry.type
class OperationSuccess:
    ok: bool


@strawberry.federation.type(keys=["id"], extend=True)
class ScheduleItemUser:
    id: strawberry.ID = strawberry.federation.field(external=True)
    full_name: str

    @classmethod
    async def resolve_reference(cls, id: str):
        user = await UsersRepository().get_by_id(int(id))

        # TODO improve error
        if not user:
            raise ValueError("No user found")

        return cls(
            id=id,
            full_name=user.fullname,
        )


@strawberry.federation.type(keys=["id"], extend=True)
class SubmissionSpeaker:
    id: strawberry.ID = strawberry.federation.field(external=True)
    full_name: str

    @classmethod
    async def resolve_reference(cls, id: str):
        user = await UsersRepository().get_by_id(int(id))

        # TODO improve error
        if not user:
            raise ValueError("No user found")

        return cls(
            id=id,
            full_name=user.fullname,
        )
