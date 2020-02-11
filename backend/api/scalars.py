from decimal import Decimal

from graphql.error import INVALID
from graphql.language.ast import StringValueNode
from graphql.type.scalars import GraphQLScalarType
from strawberry.type_converter import REGISTRY


def serialize_decimal(value):
    return str(value)


def parse_value_decimal(value):  # pragma: no cover
    return Decimal(value)


def parse_literal_decimal(ast, _variables=None):  # pragma: no cover
    if not isinstance(ast, StringValueNode):
        return INVALID

    try:
        return Decimal(ast.value)
    except ValueError:
        return INVALID


REGISTRY[Decimal] = GraphQLScalarType(
    name="Decimal",
    description="Decimal",
    serialize=serialize_decimal,
    parse_value=parse_value_decimal,
    parse_literal=parse_literal_decimal,
)
