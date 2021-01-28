from dataclasses import field, make_dataclass
from typing import List

import strawberry
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


def create_query_type(name: str, queries: List[StrawberryField]):
    cls = make_dataclass(
        name,
        fields=[
            (
                query._field_definition.origin_name,
                query._field_definition.type,
                field(default=query),
            )
            for query in queries
        ],
    )
    return strawberry.type(cls, name=name)
