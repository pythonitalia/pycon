from __future__ import annotations

from datetime import date
from typing import Optional

import strawberry

from users.domain import entities


@strawberry.type
class User:
    id: int
    fullname: str
    name: str
    email: str
    gender: str
    date_birth: Optional[date]
    open_to_recruiting: bool
    open_to_newsletter: bool
    country: str
    is_active: bool
    is_staff: bool

    @classmethod
    def from_domain(cls, entity: entities.User) -> User:
        return cls(
            id=entity.id,
            fullname=entity.fullname,
            name=entity.name,
            email=entity.email,
            gender=entity.gender,
            date_birth=entity.date_birth,
            open_to_recruiting=entity.open_to_recruiting,
            open_to_newsletter=entity.open_to_newsletter,
            country=entity.country,
            is_active=entity.is_active,
            is_staff=entity.is_staff,
        )


@strawberry.type
class SearchResults:
    users: list[User]

    @classmethod
    def from_domain(cls, users_results: list[entities.User]):
        return cls(users=[User.from_domain(user) for user in users_results])
