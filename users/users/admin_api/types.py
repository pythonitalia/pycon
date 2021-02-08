from __future__ import annotations

import strawberry

from users.domain import entities


@strawberry.type
class User:
    id: int
    fullname: str
    name: str
    email: str

    @classmethod
    def from_domain(cls, entity: entities.User) -> User:
        return cls(
            id=entity.id, fullname=entity.fullname, name=entity.name, email=entity.email
        )
