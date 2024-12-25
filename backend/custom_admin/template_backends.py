from functools import cached_property
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
        # Replace admin/base.html with a custom built template
        # that contains the Astro styles and scripts
        # allowing us to implement astro "widgets" in the Django admin

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

        # form renderer and django template renderer have some differences
        if hasattr(self, "from_string"):
            return self.from_string(text)

        return self.engine.from_string(text)


class CustomAdminDjangoTemplate(GetTemplate, DjangoTemplates):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        astro_loader_path = "custom_admin.template_backends.AstroContentLoader"

        if settings.DEBUG:
            # in debugging we don't want to cache the content
            # so we put the astro loader first
            self.engine.loaders = [astro_loader_path] + self.engine.loaders
        else:
            # When running in production, put the astro loader
            # in the Cached loader so we don't read the file every time
            # structure is: (cached_loader, [astro_loader, ... other loaders])
            self.engine.loaders[0] = (
                self.engine.loaders[0][0],
                [astro_loader_path] + self.engine.loaders[0][1],
            )


class FormRenderer(GetTemplate, FormsDjangoTemplates):
    @cached_property
    def engine(self):
        # Ugly hack because the form renderer is hardcoded here:
        # https://github.com/django/django/blob/fcd9d08379a2aee3b2c49eab0d0b8db6fd66d091/django/forms/renderers.py#L43
        # So we need to override the engine property to include the builtins
        engine = super().engine
        engine.engine.builtins = (
            engine.engine.builtins + settings.TEMPLATES[0]["OPTIONS"]["builtins"]
        )
        engine.engine.template_builtins = engine.engine.get_template_builtins(
            engine.engine.builtins
        )
        return engine
