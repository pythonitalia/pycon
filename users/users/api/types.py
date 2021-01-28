from __future__ import annotations

import strawberry
from users.domain import entities


@strawberry.type
class User:
    id: int
    email: str
    fullname: str
    name: str

    @classmethod
    def from_domain(cls, entity: entities.User) -> User:
        return cls(
            id=entity.id, email=entity.email, fullname=entity.fullname, name=entity.name
        )
