from django.urls import reverse

from notifications.tests.factories import EmailTemplateFactory
import pytest
from notifications.models import EmailTemplate
from notifications.admin.admins import EmailTemplateAdmin
from django.contrib.admin.sites import AdminSite


@pytest.mark.parametrize(
    "field_name, expected_attrs",
    [
        ("subject", {"rows": 2, "cols": 200}),
        ("preview_text", {"rows": 2, "cols": 200}),
        ("body", {"rows": 50, "cols": 200}),
    ],
)
def test_textarea_size_for_templates(rf, field_name, expected_attrs):
    db_field = EmailTemplate._meta.get_field(field_name)

    admin = EmailTemplateAdmin(
        model=EmailTemplate,
        admin_site=AdminSite(),
    )

    form_field = admin.formfield_for_dbfield(db_field, request=rf.get("/"))
    assert form_field.widget.attrs == expected_attrs


def test_cannot_edit_essential_fields_on_existing_object(rf):
    admin = EmailTemplateAdmin(
        model=EmailTemplate,
        admin_site=AdminSite(),
    )
    readonly_fields = admin.get_readonly_fields(
        request=rf.get("/"), obj=EmailTemplateFactory()
    )

    assert "conference" in readonly_fields
    assert "is_system_template" in readonly_fields
    assert "identifier" in readonly_fields


def test_can_edit_essential_fields_on_new_objects(rf):
    admin = EmailTemplateAdmin(
        model=EmailTemplate,
        admin_site=AdminSite(),
    )
    readonly_fields = admin.get_readonly_fields(request=rf.get("/"), obj=None)

    assert "conference" not in readonly_fields
    assert "is_system_template" not in readonly_fields
    assert "identifier" not in readonly_fields


def test_get_view_on_site_url():
    admin = EmailTemplateAdmin(
        model=EmailTemplate,
        admin_site=AdminSite(),
    )
    obj = EmailTemplateFactory()

    assert admin.get_view_on_site_url(obj) == reverse(
        "admin:view-email-template", args=[obj.id]
    )
    assert not admin.get_view_on_site_url(None)


def test_redirects_to_preview_when_saving_via_preview_button(rf, admin_user):
    admin = EmailTemplateAdmin(
        model=EmailTemplate,
        admin_site=AdminSite(),
    )
    obj = EmailTemplateFactory()

    request = rf.get("/")
    request.user = admin_user
    request.POST = {"_save_and_preview": "Save and preview"}

    response = admin.response_post_save_add(request, obj)
    assert response.url == reverse("admin:view-email-template", args=[obj.id])

    response = admin.response_post_save_change(request, obj)
    assert response.url == reverse("admin:view-email-template", args=[obj.id])

    request.POST = {}

    response = admin.response_post_save_change(request, obj)
    assert response.url != reverse("admin:view-email-template", args=[obj.id])

    response = admin.response_post_save_add(request, obj)
    assert response.url != reverse("admin:view-email-template", args=[obj.id])
