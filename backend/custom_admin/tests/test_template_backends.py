from custom_admin.template_backends import CustomAdminDjangoTemplate


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
