from __future__ import annotations

from datetime import date
from typing import Optional

import strawberry

from users.api.context import Info
from users.domain import entities


@strawberry.federation.type(keys=["id"])
class User:
    id: strawberry.ID
    email: str
    fullname: str
    full_name: str
    name: str

    username: str
    gender: str
    open_to_recruiting: bool
    open_to_newsletter: bool
    date_birth: Optional[date]
    country: str
    is_staff: bool

    @classmethod
    def from_domain(cls, entity: entities.User) -> User:
        return cls(
            id=entity.id,
            email=entity.email,
            fullname=entity.fullname,
            full_name=entity.fullname,
            username=entity.username,
            name=entity.name,
            gender=entity.gender,
            open_to_recruiting=entity.open_to_recruiting,
            open_to_newsletter=entity.open_to_newsletter,
            date_birth=entity.date_birth,
            country=entity.country,
            is_staff=entity.is_staff,
        )


@strawberry.type
class OperationSuccess:
    ok: bool


@strawberry.federation.type(keys=["id"], extend=True)
class ScheduleItemUser:
    id: strawberry.ID = strawberry.federation.field(external=True)
    full_name: str

    @classmethod
    async def resolve_reference(cls, info: Info, id: str):
        user = await info.context.users_dataloader.load(int(id))

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
    async def resolve_reference(cls, info: Info, id: str):
        user = await info.context.users_dataloader.load(int(id))

        # TODO improve error
        if not user:
            raise ValueError("No user found")

        return cls(
            id=id,
            full_name=user.fullname,
        )


@strawberry.federation.type(keys=["id"], extend=True)
class BlogPostAuthor:
    id: strawberry.ID = strawberry.federation.field(external=True)
    full_name: str

    @classmethod
    async def resolve_reference(cls, info: Info, id: str):
        user = await info.context.users_dataloader.load(int(id))

        # TODO improve error
        if not user:
            raise ValueError("No user found")

        return cls(
            id=id,
            full_name=user.fullname,
        )


@strawberry.federation.type(keys=["id"], extend=True)
class SubmissionCommentAuthor:
    id: strawberry.ID = strawberry.federation.field(external=True)
    is_speaker: bool = strawberry.federation.field(external=True)
    name: str

    @classmethod
    async def resolve_reference(cls, id: str, isSpeaker: bool = True):
        return cls(id=id, is_speaker=isSpeaker)

    @strawberry.federation.field(requires=["isSpeaker"])
    async def name(self, info: Info):
        name = "Speaker"

        if not self.is_speaker:
            user = await info.context.users_dataloader.load(int(self.id))

            # TODO improve error
            if not user:
                raise ValueError("No user found")

            name = user.name or user.fullname or "No name"

        return name
