import pytest
from django import forms
from django.contrib import admin

pytestmark = pytest.mark.django_db


def test_admin_url_fields_default_to_https(rf, admin_superuser):
    request = rf.get("/")
    request.user = admin_superuser
    form_classes = {}
    for model_admin in admin.site._registry.values():
        form_classes[type(model_admin).__name__] = model_admin.get_form(
            request, fields=None
        )
        for inline in model_admin.get_inline_instances(request):
            form_classes[type(inline).__name__] = inline.get_formset(
                request, fields=None
            ).form

    cleaned_urls = {
        f"{admin_name}.{field_name}": field.clean("example.com")
        for admin_name, form_class in form_classes.items()
        for field_name, field in form_class.base_fields.items()
        if isinstance(field, forms.URLField)
    }

    assert cleaned_urls
    assert {
        name: url for name, url in cleaned_urls.items() if url != "https://example.com"
    } == {}
