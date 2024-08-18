from django.urls import reverse
from django.contrib import admin
from django.urls.resolvers import URLPattern
from notifications.admin.views import view_base_template, view_sent_email
from users.admin_mixins import ConferencePermissionMixin
from django.urls import path

from notifications.models import EmailTemplate, SentEmail


@admin.register(EmailTemplate)
class EmailTemplateAdmin(ConferencePermissionMixin, admin.ModelAdmin):
    list_display = ["identifier", "name", "conference"]
    list_filter = ["identifier", "conference"]


@admin.register(SentEmail)
class SentEmailAdmin(admin.ModelAdmin):
    list_display = [
        "recipient_email",
        "sent_at",
        "email_template_display_name",
        "status",
    ]
    list_filter = ["email_template", "status"]
    search_fields = ["recipient_email"]
    readonly_fields = [
        "email_template",
        "recipient_email",
        "placeholders",
    ]
    date_hierarchy = "sent_at"
    ordering = ["-sent_at"]

    def email_template_display_name(self, obj):
        if obj.email_template.is_custom:
            return obj.email_template.name
        return obj.email_template.get_identifier_display()

    def get_urls(self) -> list[URLPattern]:
        return [
            path("view-base-template/", self.admin_site.admin_view(view_base_template)),
            path(
                "<int:object_id>/view/",
                self.admin_site.admin_view(view_sent_email),
                name="view-sent-email",
            ),
        ] + super().get_urls()

    def get_view_on_site_url(self, obj) -> str | None:
        return reverse("admin:view-sent-email", args=(obj.id,))
