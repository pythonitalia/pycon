from factory.django import DjangoModelFactory

from cms.components.sites.models import VercelFrontendSettings


class VercelFrontendSettingsFactory(DjangoModelFactory):
    class Meta:
        model = VercelFrontendSettings
