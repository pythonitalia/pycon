from custom_admin.context_processors import admin_settings


def test_admin_settings(settings, rf):
    settings.ENVIRONMENT = "test"

    output = admin_settings(rf.get("/"))
    assert output == {"CURRENT_ENV": "test"}
