from django.db import models
from wagtail.contrib.settings.models import (
    BaseSiteSetting,
    register_setting,
)


@register_setting
class VercelFrontendSettings(BaseSiteSetting):
    revalidate_url = models.CharField(max_length=3000)
    revalidate_secret = models.TextField()
