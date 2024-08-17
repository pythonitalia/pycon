import strawberry
from api.types import BaseErrorType


@strawberry.type
class SecondLevelNestedTypeError:
    second_level_1: list[str] = strawberry.field(default_factory=list)


@strawberry.type
class NestedTypeError:
    nested_field_1: list[str] = strawberry.field(default_factory=list)
    second_level: SecondLevelNestedTypeError = strawberry.field(
        default_factory=SecondLevelNestedTypeError
    )


@strawberry.type
class ArrayTypeError:
    array_field: list[str] = strawberry.field(default_factory=list)


@strawberry.type
class ErrorClass(BaseErrorType):
    @strawberry.type
    class _InnerType:
        field_1: list[str] = strawberry.field(default_factory=list)
        field_2: list[str] = strawberry.field(default_factory=list)
        field_with_type: NestedTypeError = strawberry.field(
            default_factory=NestedTypeError
        )
        field_with_array: list[ArrayTypeError] = strawberry.field(default_factory=list)

    errors: _InnerType = None


def test_error_type_with_no_errors():
    error_class = ErrorClass()

    assert not error_class.has_errors


def test_error_prefixing_errors():
    error_class = ErrorClass()

    error_class.add_error("field_1", "error message 1")

    with error_class.with_prefix("field_with_type"):
        error_class.add_error("nested_field_1", "error message 2")
        error_class.add_error("nested_field_1", "error message 3")

    with error_class.with_prefix("field_with_array.3"):
        error_class.add_error("array_field", "test 3")

    with error_class.with_prefix("field_with_array", 1):
        error_class.add_error("array_field", "test 1")

    with error_class.with_prefix("field_with_array", 1):
        error_class.add_error("array_field", "second error")

    error_class.add_error("field_1", "no prefix again")

    assert error_class.has_errors

    assert error_class.errors.field_1 == ["error message 1", "no prefix again"]
    assert error_class.errors.field_with_type.nested_field_1 == [
        "error message 2",
        "error message 3",
    ]
    assert error_class.errors.field_with_array[1].array_field == [
        "test 1",
        "second error",
    ]
    assert error_class.errors.field_with_array[3].array_field == [
        "test 3",
    ]


def test_error_type_add_error():
    error_class = ErrorClass()

    error_class.add_error("field_1", "error message 1")
    error_class.add_error("field_1", "error message 2")
    error_class.add_error("field_2", "error field 2")
    error_class.add_error("field_with_type.nested_field_1", "error nested field")
    error_class.add_error("field_with_array.3.array_field", "error field 3")
    error_class.add_error("field_with_array.5.array_field", "error array field")
    error_class.add_error("field_with_array.6.array_field", "error array field 6")

    assert error_class.has_errors
    assert error_class.errors.field_1 == ["error message 1", "error message 2"]
    assert error_class.errors.field_2 == ["error field 2"]
    assert error_class.errors.field_with_type.nested_field_1 == ["error nested field"]

    assert error_class.errors.field_with_array[0].array_field == []
    assert error_class.errors.field_with_array[1].array_field == []
    assert error_class.errors.field_with_array[2].array_field == []
    assert error_class.errors.field_with_array[3].array_field == ["error field 3"]
    assert error_class.errors.field_with_array[4].array_field == []
    assert error_class.errors.field_with_array[5].array_field == ["error array field"]
    assert error_class.errors.field_with_array[6].array_field == ["error array field 6"]
    assert len(error_class.errors.field_with_array) == 7


def test_nested_prefixes():
    error_class = ErrorClass()

    with error_class.with_prefix("field_with_type"):
        error_class.add_error("nested_field_1", "error message")
        with error_class.with_prefix("second_level"):
            error_class.add_error("second_level_1", "second level error")

    assert error_class.has_errors
    assert error_class.errors.field_with_type.nested_field_1 == ["error message"]
    assert error_class.errors.field_with_type.second_level.second_level_1 == [
        "second level error"
    ]
