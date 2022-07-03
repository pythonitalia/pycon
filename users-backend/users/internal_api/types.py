from typing import Optional

import strawberry

from users.domain import entities
from users.domain.services.create_pastaporto import create_not_authenticated_pastaporto


@strawberry.type
class User:
    id: strawberry.ID
    fullname: str
    username: Optional[str]
    name: str
    email: str
    is_active: bool
    is_staff: bool
    jwt_auth_id: int
    gender: str

    @strawberry.field
    def display_name(self) -> str:
        name = self.fullname or self.name or self.username
        return f"{name} <{self.email}>"

    @classmethod
    def from_domain(cls, user: entities.User):
        return User(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            is_staff=user.is_staff,
            jwt_auth_id=user.jwt_auth_id,
            fullname=user.fullname,
            username=user.username,
            name=user.name,
            gender=user.gender,
        )


@strawberry.type
class CreatePastaporto:
    pastaporto_token: str

    @classmethod
    def not_authenticated(cls) -> str:
        return cls(pastaporto_token=create_not_authenticated_pastaporto())
