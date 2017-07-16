import pytest
from django.apps import apps

from association.apps import AssociationConfig


def test_apps():
    assert AssociationConfig.name == 'association'
    assert apps.get_app_config('association').name == 'association'
