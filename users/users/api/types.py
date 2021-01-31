from __future__ import annotations

from typing import Generic, Optional, TypeVar

import pydantic
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


ErrorClass = TypeVar("ErrorClass")


@strawberry.type
class FieldError:
    message: str
    type: str


PydanticError = Optional[list[FieldError]]


@strawberry.type
class ValidationError(Generic[ErrorClass]):
    errors: ErrorClass

    @classmethod
    def from_validation_error(
        cls, validation_error: pydantic.ValidationError, output: ErrorClass
    ):
        errors = validation_error.errors()
        payload = {}

        for error in errors:
            field = error["loc"][0]
            message = error["msg"]
            type = error["type"]

            errors = payload.setdefault(field, [])
            errors.append(FieldError(message=message, type=type))

        return cls(errors=output(**payload))
