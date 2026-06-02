import pytest
from django.test import RequestFactory

from custom_admin.index import OTHER_GROUP, build_groups, custom_index


@pytest.fixture
def admin_request(admin_user):
    # The project's admin_user is staff-only; make it a superuser so it sees
    # every registered model in get_app_list.
    admin_user.is_superuser = True
    admin_user.save()
    request = RequestFactory().get("/admin/")
    request.user = admin_user
    return request


def test_index_returns_groups_and_quick_links(admin_request):
    # Inspect context_data directly so we don't render the Astro admin base,
    # which isn't available in the test environment.
    response = custom_index(admin_request)

    assert "groups" in response.context_data
    assert "quick_links" in response.context_data
    assert len(response.context_data["groups"]) > 0


def test_every_registered_model_appears_exactly_once(admin_request):
    response = custom_index(admin_request)

    app_models = [
        model["object_name"]
        for app in response.context_data["app_list"]
        for model in app["models"]
    ]
    grouped_models = [
        model["object_name"]
        for group in response.context_data["groups"]
        for model in group["models"]
    ]

    # No model dropped, none duplicated across groups.
    assert sorted(grouped_models) == sorted(app_models)


def test_unmapped_model_falls_through_to_other():
    fake_app_list = [
        {
            "app_label": "mystery",
            "name": "Mystery",
            "models": [
                {"object_name": "SomethingBrandNew", "name": "Something brand new"}
            ],
        }
    ]

    groups = build_groups(fake_app_list)

    assert len(groups) == 1
    assert groups[0]["title"] == OTHER_GROUP
    assert groups[0]["models"][0]["object_name"] == "SomethingBrandNew"


def test_context_is_json_serializable_for_astro_props(admin_request):
    # The Astro page passes these through the `to_json_for_prop` filter, so they
    # must survive json serialization (no model classes / lazy strings leaking).
    from custom_admin.templatetags.to_json_for_prop import to_json_for_prop

    response = custom_index(admin_request)

    for key in ("groups", "all_apps", "quick_links", "breadcrumbs"):
        # Raises if the value isn't serializable.
        assert to_json_for_prop(response.context_data[key]) is not None


def test_quick_links_resolve_to_urls(admin_request):
    response = custom_index(admin_request)

    quick_links = response.context_data["quick_links"]
    titles = {link["title"] for link in quick_links}

    assert {"Review grants", "Review submissions"} <= titles
    assert all(link["url"] for link in quick_links)
