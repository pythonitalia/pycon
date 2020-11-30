from datetime import date, datetime, time
import enum
from typing import List, Optional

import pytest
import strawberry
from django.core.exceptions import ImproperlyConfigured
from django.forms import (
    BooleanField,
    CharField,
    ChoiceField,
    DateField,
    DateTimeField,
    DecimalField,
    EmailField,
    Field,
    FloatField,
    IntegerField,
    ModelMultipleChoiceField,
    NullBooleanField,
    SlugField,
    TimeField,
    URLField,
    UUIDField,
)
from django.forms.fields import BaseTemporalField
from strawberry_forms.converter import convert_form_field
from strawberry_forms.mutations import convert_enums_to_values

CONVERT_MAP = {
    CharField: str,
    BaseTemporalField: str,
    EmailField: str,
    SlugField: str,
    URLField: str,
    ChoiceField: str,
    # RegexField: str,
    Field: str,
    UUIDField: str,  # UUID
    IntegerField: int,
    # NumberInput: Int,
    DecimalField: float,
    FloatField: float,
    DateField: date,
    DateTimeField: datetime,
    TimeField: time,
}


def test_convert_char_field():
    for origin, destination in CONVERT_MAP.items():
        base_conv = convert_form_field(origin())

        assert base_conv[0] == destination, origin

        with_required = convert_form_field(origin(required=True))

        assert with_required[0] == destination, origin


def test_convert_boolean():
    nonnull_boolean = convert_form_field(BooleanField())

    assert nonnull_boolean[0] == bool

    null_boolean = convert_form_field(NullBooleanField())

    assert null_boolean[0] == Optional[bool]


def test_convert_custom_not_registered_type():
    class TestField:
        pass

    field = TestField()

    with pytest.raises(ImproperlyConfigured) as e:
        convert_form_field(field)

    message = (
        "Don't know how to convert the Django form field "
        f"{field} ({field.__class__}) to type"
    )

    assert message in str(e.value)


def test_convert_multiple_model_choice_field():
    base_conv = convert_form_field(ModelMultipleChoiceField(queryset=None))

    assert base_conv[0] == List[strawberry.ID]
    assert base_conv[0].__args__[0] == strawberry.ID

    not_required = convert_form_field(
        ModelMultipleChoiceField(queryset=None, required=False)
    )

    assert not_required[0] == Optional[List[strawberry.ID]]
    assert not_required[0].__args__[0].__args__[0] == strawberry.ID


def test_enum_convert_util():
    class Example(enum.Enum):
        TEST = "test"

    value = {"data": {"enum": Example.TEST}, "enum": Example.TEST}

    assert convert_enums_to_values(value) == {"data": {"enum": "test"}, "enum": "test"}
