from django.template import TemplateDoesNotExist
from django.template.backends.django import DjangoTemplates
from django.template.backends.django import reraise, Template as BaseTemplate
from django.conf import settings
from urllib.parse import urlencode


class CustomAdminDjangoTemplate(DjangoTemplates):
    def get_template(self, template_name):
        if not template_name.startswith("astro/"):
            return super().get_template(template_name)

        if not settings.DEBUG:
            return super().get_template(template_name)

        path = template_name.split("/")[1].replace(".html", "")
        try:
            return Template(
                template=self.engine.get_template("admin/iframe.html"),
                backend=self,
                template_name=path,
            )
        except TemplateDoesNotExist as exc:
            reraise(exc, self)


class Template(BaseTemplate):
    def __init__(self, template_name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.template_name = template_name

    def render(self, context=None, request=None):
        context["TEMPLATE_NAME"] = self.template_name
        context["ASTRO_ARGS"] = urlencode({**context.get("arguments", {})})
        return super().render(context=context, request=request)
