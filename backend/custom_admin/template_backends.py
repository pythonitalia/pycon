import requests
from django.template.backends.django import (
    DjangoTemplates,
)
from django.forms.renderers import DjangoTemplates as FormsDjangoTemplates
from django.template.loaders.base import Loader
from django.template import Origin

from django.conf import settings


def _proxy_to_astro(template_name):
    # template_name contains astro/ in the name
    # which will end up in the view `astro_proxy`
    # which forwards the request to the astro server
    response = requests.get(f"http://127.0.0.1:8000/{template_name}")
    response.raise_for_status()
    return response.text


def _can_be_proxied(template_name):
    if not settings.DEBUG:
        return False

    return template_name == "admin/base.html" or template_name.startswith("astro/")


class AstroContentLoader(Loader):
    def get_template_sources(self, template_name):
        # We make admin/base.html to be proxied to astro/admin-base.html
        # so that Astro can add styles and scripts to the page
        if template_name == "admin/base.html":
            yield Origin(
                name=template_name,
                template_name="astro/admin-base.html",
                loader=self,
            )

    def get_contents(self, origin):
        template_name = origin.template_name

        if not _can_be_proxied(template_name):
            return open("custom_admin/templates/" + template_name).read()

        return _proxy_to_astro(template_name)


class GetTemplate:
    def get_template(self, template_name):
        if not _can_be_proxied(template_name):
            return super().get_template(template_name)

        text = _proxy_to_astro(template_name)

        if hasattr(self, "from_string"):
            return self.from_string(text)

        return self.engine.from_string(text)


class CustomAdminDjangoTemplate(GetTemplate, DjangoTemplates):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.engine.loaders = [
            "custom_admin.template_backends.AstroContentLoader",
        ] + self.engine.loaders


class FormRenderer(GetTemplate, FormsDjangoTemplates):
    ...
