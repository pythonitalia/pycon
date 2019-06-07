import pytest

from django.forms import (
    CharField, EmailField, SlugField,
    URLField, ChoiceField, RegexField,
    Field, UUIDField, IntegerField,
    NumberInput, DecimalField, FloatField,
    DateField, DateTimeField, TimeField,
    BooleanField, NullBooleanField,
    ModelMultipleChoiceField,
)
from django.core.exceptions import ImproperlyConfigured
from django.forms.fields import BaseTemporalField

from graphene import ID, Boolean, Float, Int, List, String, UUID, Date, DateTime, Time

from graphene_form.converter import convert_form_field


CONVERT_MAP = {
    CharField: String,
    BaseTemporalField: String,
    EmailField: String,
    SlugField: String,
    URLField: String,
    ChoiceField: String,
    # RegexField: String,
    Field: String,

    UUIDField: UUID,

    IntegerField: Int,
    # NumberInput: Int,

    DecimalField: Float,
    FloatField: Float,

    DateField: Date,
    DateTimeField: DateTime,
    TimeField: Time,
}

def test_convert_char_field():
    for origin, destination in CONVERT_MAP.items():
        base_conv = convert_form_field(origin())

        assert isinstance(base_conv, destination)
        assert base_conv.kwargs['description'] == ''
        assert base_conv.kwargs['required'] is True

        with_help_text = convert_form_field(origin(help_text='Help me!'))

        assert isinstance(with_help_text, destination)
        assert with_help_text.kwargs['description'] == 'Help me!'
        assert with_help_text.kwargs['required'] is True

        with_required = convert_form_field(origin(required=True))

        assert isinstance(with_required, destination)
        assert with_required.kwargs['description'] == ''
        assert with_required.kwargs['required'] is True

        with_both = convert_form_field(origin(required=False, help_text='Help me!'))

        assert isinstance(with_both, destination)
        assert with_both.kwargs['description'] == 'Help me!'
        assert with_both.kwargs['required'] is False


def test_convert_boolean():
    nonnull_boolean = convert_form_field(BooleanField())

    assert isinstance(nonnull_boolean, Boolean)
    assert nonnull_boolean.kwargs['description'] == ''
    assert nonnull_boolean.kwargs['required'] is True

    nonnull_boolean_with_desc = convert_form_field(BooleanField(help_text='eeeeeeeeeeeeeeewwwwwwww'))

    assert isinstance(nonnull_boolean_with_desc, Boolean)
    assert nonnull_boolean_with_desc.kwargs['description'] == 'eeeeeeeeeeeeeeewwwwwwww'
    assert nonnull_boolean_with_desc.kwargs['required'] is True

    null_boolean = convert_form_field(NullBooleanField())

    assert isinstance(null_boolean, Boolean)
    assert null_boolean.kwargs['description'] == ''
    assert null_boolean.kwargs['required'] is False

    null_boolean_with_desc = convert_form_field(NullBooleanField(help_text='aaaaaaaaaaaaaaaaaaawwwwwwwww'))

    assert isinstance(null_boolean_with_desc, Boolean)
    assert null_boolean_with_desc.kwargs['description'] == 'aaaaaaaaaaaaaaaaaaawwwwwwwww'
    assert null_boolean_with_desc.kwargs['required'] is False


def test_convert_custom_not_registered_type():
    class TestField:
        pass

    field = TestField()

    with pytest.raises(ImproperlyConfigured) as e:
        convert_form_field(field)

    assert "Don't know how to convert the Django form field %s (%s) to Graphene type" % (field, field.__class__) in str(e)


def test_convert_multiple_model_choice_field():
    base_conv = convert_form_field(ModelMultipleChoiceField(queryset=None))

    assert isinstance(base_conv, List)
    assert base_conv._of_type.__name__ == 'ID'
    assert base_conv.kwargs['required'] is True

    not_required = convert_form_field(ModelMultipleChoiceField(queryset=None, required=True))

    assert isinstance(not_required, List)
    assert not_required._of_type.__name__ == 'ID'
    assert not_required.kwargs['required'] is True
