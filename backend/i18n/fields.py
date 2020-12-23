# flake8: noqa

import json

import django
from django.conf import settings
from django.db.models import JSONField

from .forms import I18nFormField, I18nTextarea, I18nTextInput
from .strings import LazyI18nString


class I18nFieldMixin:
    form_class = I18nFormField
    widget = I18nTextInput

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop("event", None)
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, LazyI18nString):
            return value
        if value is None:
            return None
        return value

    def get_prep_value(self, value):
        if isinstance(value, LazyI18nString):
            value = value.data
        if isinstance(value, dict):
            return json.dumps({k: v for k, v in value.items() if v}, sort_keys=True)
        if isinstance(value, LazyI18nString.LazyGettextProxy):
            return json.dumps(
                {lng: value[lng] for lng, lngname in settings.LANGUAGES if value[lng]},
                sort_keys=True,
            )
        return value

    def get_prep_lookup(self, lookup_type, value):  # NOQA
        raise TypeError("Lookups on i18n strings are currently not supported.")

    # def get_db_prep_value(self, value, connection, prepared=False):
    #     return super().get_db_prep_value(value, connection, prepared)

    if django.VERSION < (2,):

        def from_db_value(self, value, expression, connection, context):
            return LazyI18nString(value)

    else:

        def from_db_value(self, value, expression, connection):
            return LazyI18nString(value)

    def formfield(self, **kwargs):
        defaults = {"form_class": self.form_class, "widget": self.widget}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class I18nCharField(I18nFieldMixin, JSONField):
    """
    A CharField which takes internationalized data. Internally, a TextField dabase
    field is used to store JSON. If you interact with this field, you will work
    with LazyI18nString instances.
    """

    widget = I18nTextInput


class I18nTextField(I18nFieldMixin, JSONField):
    """
    Like I18nCharField, but for TextFields.
    """

    widget = I18nTextarea
