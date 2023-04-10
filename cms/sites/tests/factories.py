from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from sites.models import VercelFrontendSettings


@register
class VercelFrontendSettingsFactory(DjangoModelFactory):
    class Meta:
        model = VercelFrontendSettings
