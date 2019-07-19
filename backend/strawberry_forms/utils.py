import dataclasses
from collections import OrderedDict
from typing import List

import strawberry

from .converter import convert_form_field


def convert_form_fields_to_fields(form_fields):
    fields = OrderedDict()

    for name, field in form_fields.items():
        fields[name] = convert_form_field(field)

    return fields


def create_input_type(base_name, graphql_fields):
    input_class = dataclasses.make_dataclass(
        f"{base_name}Input",
        [(name, type_, field) for name, [type_, field] in graphql_fields.items()],
    )
    return strawberry.input(input_class)


def create_error_type(base_name, graphql_fields):
    fields = [
        (name, List[str], dataclasses.field(default_factory=list))
        for name, _ in graphql_fields.items()
    ]
    fields.append(
        ("nonFieldErrors", List[str], dataclasses.field(default_factory=list))
    )

    error_type = dataclasses.make_dataclass(f"{base_name}Errors", fields)
    return strawberry.type(error_type)
