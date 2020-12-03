import strawberry

from dataclasses import field, make_dataclass
from typing import List

from strawberry.field import StrawberryField


def create_mutation_type(name: str, mutations: List[StrawberryField]):
    cls = make_dataclass(
        name,
        fields=[
            (
                mutation._field_definition.name
                or mutation._field_definition.origin_name,
                mutation._field_definition.type,
                field(default=strawberry.mutation(mutation._field_definition.origin)),
            )
            for mutation in mutations
        ],
    )

    return strawberry.type(cls, name=name)
