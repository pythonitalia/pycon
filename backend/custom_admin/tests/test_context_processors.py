from custom_admin.context_processors import admin_settings, astro_settings


def test_admin_settings(settings, rf):
    settings.ENVIRONMENT = "test"

    output = admin_settings(rf.get("/"))
    assert output == {"CURRENT_ENV": "test"}


def test_astro_settings(rf):
    request = rf.get("/")
    output = astro_settings(request)
    assert output == {
        "ASTRO_URL": "http://testserver/astro",
        "APOLLO_GRAPHQL_URL": "/admin/graphql",
    }
