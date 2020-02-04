from functools import singledispatch
from typing import List, Optional

import strawberry
from django import forms
from django.core.exceptions import ImproperlyConfigured
from strawberry.types.datetime import DateTime


@singledispatch
def convert_form_field(field):
    raise ImproperlyConfigured(
        "Don't know how to convert the Django form field %s (%s) "
        "to type" % (field, field.__class__)
    )


def type_or_optional_wrapped(type_, required):
    if required:
        return type_

    return Optional[type_]


@convert_form_field.register(forms.fields.BaseTemporalField)
@convert_form_field.register(forms.CharField)
@convert_form_field.register(forms.EmailField)
@convert_form_field.register(forms.SlugField)
@convert_form_field.register(forms.URLField)
@convert_form_field.register(forms.ChoiceField)
@convert_form_field.register(forms.RegexField)
@convert_form_field.register(forms.Field)
def convert_form_field_to_string(field):
    return (
        type_or_optional_wrapped(str, field.required),
        strawberry.field(description=field.help_text, is_input=True),
    )


@convert_form_field.register(forms.UUIDField)
def convert_form_field_to_uuid(field):
    return (
        type_or_optional_wrapped(str, field.required),
        strawberry.field(description=field.help_text, is_input=True),
    )


@convert_form_field.register(forms.IntegerField)
@convert_form_field.register(forms.NumberInput)
def convert_form_field_to_int(field):
    return (
        type_or_optional_wrapped(int, field.required),
        strawberry.field(description=field.help_text, is_input=True),
    )


@convert_form_field.register(forms.BooleanField)
def convert_form_field_to_boolean(field):
    return (bool, strawberry.field(description=field.help_text, is_input=True))


@convert_form_field.register(forms.NullBooleanField)
def convert_form_field_to_nullboolean(field):
    return (
        Optional[bool],
        strawberry.field(description=field.help_text, is_input=True),
    )


@convert_form_field.register(forms.DecimalField)
@convert_form_field.register(forms.FloatField)
def convert_form_field_to_float(field):
    return (
        type_or_optional_wrapped(float, field.required),
        strawberry.field(description=field.help_text, is_input=True),
    )


@convert_form_field.register(forms.ModelMultipleChoiceField)
def convert_form_field_to_list(field):
    return (
        type_or_optional_wrapped(List[strawberry.ID], field.required),
        strawberry.field(description=field.help_text, is_input=True),
    )


@convert_form_field.register(forms.DateField)
def convert_form_field_to_date(field):
    return (
        type_or_optional_wrapped(str, field.required),
        strawberry.field(description=field.help_text, is_input=True),
    )


@convert_form_field.register(forms.DateTimeField)
def convert_form_field_to_datetime(field):
    return (
        type_or_optional_wrapped(DateTime, field.required),
        strawberry.field(description=field.help_text, is_input=True),
    )


@convert_form_field.register(forms.TimeField)
def convert_form_field_to_time(field):
    return (
        type_or_optional_wrapped(str, field.required),
        strawberry.field(description=field.help_text, is_input=True),
    )


@convert_form_field.register(forms.ModelChoiceField)
def convert_form_field_to_id(field):
    return (
        type_or_optional_wrapped(strawberry.ID, field.required),
        strawberry.field(description=field.help_text, is_input=True),
    )
