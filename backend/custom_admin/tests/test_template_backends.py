import pytest
from unittest.mock import Mock, mock_open, patch
from custom_admin.template_backends import (
    AstroContentLoader,
    CustomAdminDjangoTemplate,
    FormRenderer,
)


def test_get_template_in_dev_mode(settings, requests_mock):
    mock_req = requests_mock.get(
        "http://127.0.0.1:8000/astro/test.html", text="Hello, Astro!"
    )
    settings.DEBUG = True

    backend = CustomAdminDjangoTemplate(
        {"NAME": "", "DIRS": [], "APP_DIRS": False, "OPTIONS": {}}
    )
    result = backend.get_template("astro/test.html")
    assert result.render() == "Hello, Astro!"
    assert mock_req.called


def test_form_renderer_template(settings, requests_mock):
    mock_req = requests_mock.get(
        "http://127.0.0.1:8000/astro/test.html", text="Hello form!"
    )
    settings.DEBUG = True

    backend = FormRenderer()
    result = backend.get_template("astro/test.html")
    assert result.render() == "Hello form!"
    assert mock_req.called


def test_astro_content_loader_loads_from_disk_in_prod(settings):
    settings.DEBUG = False

    loader = AstroContentLoader(engine=Mock())
    origin = loader.get_template_sources("admin/base.html")
    origin = next(origin)

    with patch("builtins.open", mock_open(read_data="Hello from disk!")) as mock_file:
        contents = loader.get_contents(origin)

    assert contents == "Hello from disk!"
    mock_file.assert_called_once_with("custom_admin/templates/astro/admin-base.html")


def test_astro_content_loader_proxies_admin_base_to_astro_in_dev(
    settings, requests_mock
):
    settings.DEBUG = True
    mock_req = requests_mock.get(
        "http://127.0.0.1:8000/astro/admin-base.html", text="Hello, Astro!"
    )

    loader = AstroContentLoader(engine=Mock())
    origin = loader.get_template_sources("admin/base.html")
    origin = next(origin)

    assert origin.name == "admin/base.html"
    assert origin.template_name == "astro/admin-base.html"
    assert origin.loader == loader

    contents = loader.get_contents(origin)

    assert contents == "Hello, Astro!"
    assert mock_req.called


@pytest.mark.parametrize("template_name", ["admin/test.html", "other-template.html"])
def test_astro_content_loader_ignores_non_admin_base_templates(settings, template_name):
    settings.DEBUG = True

    loader = AstroContentLoader(engine=Mock())
    with pytest.raises(StopIteration):
        next(loader.get_template_sources(template_name))
