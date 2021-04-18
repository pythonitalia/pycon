from dataclasses import field as dataclasses_field
from dataclasses import make_dataclass
from typing import Type

import pydantic
import strawberry
from strawberry.field import StrawberryField

from .types import FieldError


def create_root_type(fields: list[StrawberryField]) -> Type:
    cls = make_dataclass(
        "RootType",
        fields=[
            (
                field.graphql_name,
                field.type,
                dataclasses_field(default=field),
            )  # type: ignore
            for field in fields
        ],
    )

    return strawberry.type(cls)


def create_validation_error_type(prefix: str, type_: StrawberryField):
    @classmethod
    def from_validation_error(cls, validation_error: pydantic.ValidationError):
        errors = validation_error.errors()
        payload = {}

        for error in errors:
            field = error["loc"][0]
            message = error["msg"]
            error_type = error["type"]

            errors = payload.setdefault(field, [])
            errors.append(FieldError(message=message, type=error_type))

        return cls(errors=type_(**payload))

    cls = make_dataclass(f"{prefix}ValidationError", [("errors", type_)])
    cls.from_validation_error = from_validation_error
    return strawberry.type(cls)
