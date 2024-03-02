from django.urls import reverse


def test_astro_proxy_is_disabled_in_prod(admin_client, settings):
    settings.DEBUG = False

    response = admin_client.get(reverse("astro-proxy", kwargs={"path": "test"}))

    assert response.status_code == 404


def test_astro_proxy(admin_client, requests_mock, settings):
    settings.DEBUG = True

    requests_mock.get(
        "http://custom-admin:3002/test",
        text='<script type="module" src="/test.js"></script>',
    )

    response = admin_client.get(reverse("astro-proxy", kwargs={"path": "test"}))

    assert response.status_code == 200
    assert (
        response.content.decode("utf-8")
        == '<script type="module" src="/astro/test.js"></script>'
    )


def test_astro_proxy_redirection(admin_client, requests_mock, settings):
    settings.DEBUG = True

    requests_mock.get(
        "http://custom-admin:3002/test",
        headers={"Location": "/redirect"},
        status_code=302,
    )

    requests_mock.get(
        "http://custom-admin:3002/redirect",
        text='<script type="module" src="/redirect.js"></script>',
    )

    response = admin_client.get(reverse("astro-proxy", kwargs={"path": "test"}))

    assert response.status_code == 200
    assert (
        response.content.decode("utf-8")
        == '<script type="module" src="/astro/redirect.js"></script>'
    )
