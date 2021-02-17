from dataclasses import field, make_dataclass
from typing import List

import pydantic
import strawberry
from association.api.mutation.types import FieldError
from strawberry.field import StrawberryField


def create_mutation_type(name: str, mutations: List[StrawberryField]):
    cls = make_dataclass(
        name,
        fields=[
            (
                mutation._field_definition.origin_name,
                mutation._field_definition.type,
                field(default=strawberry.mutation(mutation._field_definition.origin)),
            )
            for mutation in mutations
        ],
    )

    return strawberry.type(cls, name=name)


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
