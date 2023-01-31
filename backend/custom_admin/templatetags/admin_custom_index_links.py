from django import template
from django.conf import settings
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from custom_admin.admin import CustomIndexLinks

register = template.Library()


@register.simple_tag
def admin_custom_index_links(app):
    outputs = []
    STATIC_URL = settings.STATIC_URL

    for model, admin_instance in admin.site._registry.items():
        app_name = app.get("app_label", app["name"].lower())
        if app_name not in str(model._meta):
            continue

        if isinstance(admin_instance, CustomIndexLinks):
            for custom_index_link in admin_instance.get_index_links():
                admin_url = reverse(f"admin:custom_index_link_{custom_index_link[1]}")
                outputs.append(
                    (
                        "%sadmin_views/icons/view.png" % STATIC_URL,
                        admin_url,
                        custom_index_link[0],
                    )
                )

    return mark_safe(
        format_html_join(
            "",
            """<tr>
                <th scope="row">
                    <img src="{}" alt="" />
                    <a href="{}">{}</a>
                </th>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
            </tr>""",
            outputs,
        )
    )
