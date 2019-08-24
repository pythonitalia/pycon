import datetime
from decimal import Decimal
from typing import NewType

from aniso8601 import parse_date, parse_datetime
from graphql.error import INVALID
from graphql.language.ast import StringValueNode
from graphql.type.scalars import GraphQLScalarType
from strawberry.type_converter import REGISTRY

DateTime = NewType("DateTime", str)


def serialize_datetime(value):
    return value.isoformat()


def parse_value_datetime(value):
    return parse_datetime(value)


def parse_literal_datetime(ast, _variables=None):
    if not isinstance(ast, StringValueNode):
        return INVALID

    try:
        return parse_datetime(ast.value)
    except ValueError:
        return INVALID


REGISTRY[DateTime] = GraphQLScalarType(
    name="DateTime",
    description="Date with time (isoformat)",
    serialize=serialize_datetime,
    parse_value=parse_value_datetime,
    parse_literal=parse_literal_datetime,
)


Date = NewType("Date", str)


def serialize_date(value):
    if isinstance(value, datetime.datetime):
        value = value.date()

    return value.isoformat()


def parse_value_date(value):
    return parse_date(value)


def parse_literal_date(ast, _variables=None):
    if not isinstance(ast, StringValueNode):
        return INVALID

    try:
        return parse_date(ast.value)
    except ValueError:
        return INVALID


REGISTRY[Date] = GraphQLScalarType(
    name="Date",
    description="Date",
    serialize=serialize_date,
    parse_value=parse_value_date,
    parse_literal=parse_literal_date,
)


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
