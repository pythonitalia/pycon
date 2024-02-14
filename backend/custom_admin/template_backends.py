from django.template import TemplateDoesNotExist
from django.template.backends.django import DjangoTemplates
from django.template.backends.django import reraise, Template as BaseTemplate
from django.conf import settings
from urllib.parse import urlencode


class CustomAdminDjangoTemplate(DjangoTemplates):
    def get_template(self, template_name):
        if not template_name.startswith("astro/"):
            return super().get_template(template_name)

        astro_path = template_name.split("/")[1].replace(".html", "")

        if settings.DEBUG:
            template_name = "admin/iframe.html"

        try:
            return Template(
                template=self.engine.get_template(template_name),
                backend=self,
                astro_path=astro_path,
            )
        except TemplateDoesNotExist as exc:
            reraise(exc, self)


class Template(BaseTemplate):
    def __init__(self, astro_path: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.astro_path = astro_path

    def render(self, context=None, request=None):
        context = {
            "ASTRO_PATH": self.astro_path,
            "ASTRO_URL_ARGS": urlencode({**context.get("arguments", {})}),
            **context.get("arguments", {}),
        }
        return super().render(context=context, request=request)
