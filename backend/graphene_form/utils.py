from collections import OrderedDict

from graphene import ObjectType, InputObjectType, String, List, NonNull

from .converter import convert_form_field


def convert_form_fields_to_fields(form_fields):
    fields = OrderedDict()

    for name, field in form_fields.items():
        fields[name] = convert_form_field(field)

    return fields


def create_input_type(base_name, graphql_fields):
    return type(
        f'{base_name}Input',
        (InputObjectType,),
        OrderedDict(graphql_fields)
    )


def create_errors_type(base_name, graphql_fields):
    error_fields = {name: List(NonNull(String)) for name in graphql_fields.keys()}

    return type(
        f'{base_name}Errors',
        (ObjectType, ),
        OrderedDict(error_fields)
    )
