from datetime import date, datetime

from api.scalars import (
    parse_literal_date,
    parse_literal_datetime,
    parse_value_date,
    parse_value_datetime,
    serialize_date,
    serialize_datetime,
)
from graphql.error import INVALID
from graphql.language.ast import IntValueNode, StringValueNode
from pytest import raises


def test_datetime_is_converted_in_isoformat():
    assert serialize_datetime(datetime(1995, 1, 1, 1, 1)) == "1995-01-01T01:01:00"


def test_parse_datetime_string_to_datetime():
    as_string = "1995-01-01T01:01:00"

    assert parse_value_datetime(as_string) == datetime(1995, 1, 1, 1, 1)


def test_parse_invalid_datetime():
    as_string = "11111"

    with raises(ValueError):
        parse_value_datetime(as_string)


def test_parse_datetime_from_ast():
    node = StringValueNode()
    node.value = "1995-01-01T01:01:00"

    assert parse_literal_datetime(node) == datetime(1995, 1, 1, 1, 1)


def test_parse_datetime_from_invalid_ast_value():
    node = StringValueNode()
    node.value = "11111"

    assert parse_literal_datetime(node) == INVALID


def test_parse_datetime_using_invalid_ast_node():
    node = IntValueNode()
    node.value = 10

    assert parse_literal_datetime(node) == INVALID


def test_serialize_date_datetime_is_converted_in_date_isoformat():
    assert serialize_date(datetime(1995, 1, 1)) == "1995-01-01"


def test_serialize_date_is_converted_in_isoformat():
    assert serialize_date(date(1995, 1, 1)) == "1995-01-01"


def test_parse_date_string_to_datetime():
    as_string = "1995-01-01"

    assert parse_value_date(as_string) == date(1995, 1, 1)


def test_parse_invalid_date():
    as_string = "11111"

    with raises(ValueError):
        parse_value_date(as_string)


def test_parse_date_from_ast():
    node = StringValueNode()
    node.value = "1995-01-01"

    assert parse_literal_date(node) == date(1995, 1, 1)


def test_parse_date_from_invalid_ast_value():
    node = StringValueNode()
    node.value = "11111"

    assert parse_literal_date(node) == INVALID


def test_parse_date_using_invalid_ast_node():
    node = IntValueNode()
    node.value = 10

    assert parse_literal_date(node) == INVALID
