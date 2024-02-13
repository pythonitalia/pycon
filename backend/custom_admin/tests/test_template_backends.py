from unittest.mock import Mock
from custom_admin.template_backends import CustomAdminDjangoTemplate


def test_get_template_in_dev_mode(settings):
    settings.DEBUG = True

    backend = CustomAdminDjangoTemplate(
        {"NAME": "", "DIRS": [], "APP_DIRS": False, "OPTIONS": {}}
    )
    backend.engine = Mock()
    backend.get_template("astro/test.html")
    backend.engine.get_template.assert_called_with("admin/iframe.html")
