from datetime import datetime
from typing import Optional

import strawberry
from api.context import Info
from api.types import User
from domain import entities


@strawberry.type
class Query:
    @strawberry.field
    async def me(self, info: Info, id: int) -> Optional[User]:
        user = await info.context.users_repository.get(id)
        return User.from_domain(user) if user else None


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_user(self, info: Info) -> User:
        user = await info.context.users_repository.save_user(
            entities.User(
                # id=45,
                username="Marco",
                email="marcoaciernoemail@gmail.com",
                password="hello",
                fullname="Marco Test",
                name="Marco",
                gender="male",
                date_birth=datetime.now().date(),
                open_to_newsletter=False,
                open_to_recruiting=False,
                country="UK",
                date_joined=datetime.now(),
                is_active=True,
                is_staff=False,
            )
        )
        return User.from_domain(user)


schema = strawberry.federation.Schema(Query, Mutation)
