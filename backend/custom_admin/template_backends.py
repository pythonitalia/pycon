import requests
from django.template import TemplateDoesNotExist
from django.template.backends.django import (
    DjangoTemplates,
    reraise,
    Template as BaseTemplate,
)
from django.template import Template

from django.conf import settings


class CustomAdminDjangoTemplate(DjangoTemplates):
    def get_template(self, template_name):
        if not template_name.startswith("astro/") or not settings.DEBUG:
            return super().get_template(template_name)

        # Proxy the request to Astro
        response = requests.get(f"http://127.0.0.1:8000/{template_name}")

        try:
            return BaseTemplate(Template(response.text), backend=self)
        except TemplateDoesNotExist as exc:
            reraise(exc, self)
