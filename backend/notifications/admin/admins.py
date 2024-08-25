from typing import Any
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.urls import reverse
from django.contrib import admin
from django.urls.resolvers import URLPattern
from notifications.admin.views import (
    view_empty_template,
    view_sent_email,
    view_email_template,
)
from users.admin_mixins import ConferencePermissionMixin
from django.urls import path
from django.utils.safestring import mark_safe

from notifications.models import EmailTemplate, SentEmail, SentEmailEvent
from django.forms import Textarea


class SentEmailEventInline(admin.TabularInline):
    model = SentEmailEvent
    extra = 0
    fields = ["event", "timestamp", "payload"]
    readonly_fields = ["event", "timestamp", "payload"]
    ordering = ["timestamp"]
    show_change_link = False
    verbose_name = "Event"
    verbose_name_plural = "Events"


@admin.register(EmailTemplate)
class EmailTemplateAdmin(ConferencePermissionMixin, admin.ModelAdmin):
    list_display = ["identifier", "name", "conference"]
    list_filter = ["identifier", "conference"]
    fields = [
        "conference",
        "identifier",
        "name",
        "placeholders_available",
        "subject",
        "preview_text",
        "body",
        "reply_to",
        "cc_addresses",
        "bcc_addresses",
        "save_and_preview",
    ]
    readonly_fields = ["save_and_preview", "placeholders_available"]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "body":
            kwargs["widget"] = Textarea(attrs={"rows": 50, "cols": 200})

        if db_field.name in ("subject", "preview_text"):
            kwargs["widget"] = Textarea(attrs={"rows": 2, "cols": 200})

        return super().formfield_for_dbfield(db_field, **kwargs)

    def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...):
        fields = super().get_readonly_fields(request, obj)

        if obj:
            fields = fields + ["conference", "identifier"]

        return fields

    def response_post_save_add(self, request, obj):
        """
        Figure out where to redirect after the 'Save' button has been pressed
        when adding a new object.
        """
        if "_save_and_preview" in request.POST:
            return HttpResponseRedirect(
                reverse("admin:view-email-template", args=[obj.id])
            )
        return self._response_post_save(request, obj)

    def response_post_save_change(self, request, obj):
        if "_save_and_preview" in request.POST:
            return HttpResponseRedirect(
                reverse("admin:view-email-template", args=[obj.id])
            )

        return self._response_post_save(request, obj)

    def save_and_preview(self, obj):
        return mark_safe(
            '<input type="submit" name="_save_and_preview" value="Save and preview" />'
        )

    def placeholders_available(self, obj):
        return mark_safe(
            "<br>".join(
                [
                    "{{" + placeholder + "}}"
                    for placeholder in obj.get_placeholders_available()
                ]
            )
        )

    def get_urls(self) -> list[URLPattern]:
        return [
            path(
                "view-empty-template/", self.admin_site.admin_view(view_empty_template)
            ),
            path(
                "<int:object_id>/view/",
                self.admin_site.admin_view(view_email_template),
                name="view-email-template",
            ),
        ] + super().get_urls()

    def get_view_on_site_url(self, obj) -> str | None:
        return reverse("admin:view-email-template", args=(obj.id,))


@admin.register(SentEmail)
class SentEmailAdmin(admin.ModelAdmin):
    list_display = [
        "recipient_email",
        "sent_at",
        "email_template_display_name",
        "status",
        "message_id",
    ]
    list_filter = ["email_template", "status"]
    search_fields = ["recipient_email"]
    fields = [
        "conference",
        "status",
        "sent_at",
        "message_id",
        "recipient",
        "recipient_email",
        "subject",
        "preview_text",
        "placeholders",
        "reply_to",
        "cc_addresses",
        "bcc_addresses",
        "email_template",
    ]
    date_hierarchy = "sent_at"
    ordering = ["-sent_at"]
    autocomplete_fields = ["recipient"]
    inlines = [SentEmailEventInline]

    def email_template_display_name(self, obj):
        if obj.email_template.is_custom:
            return obj.email_template.name
        return obj.email_template.get_identifier_display()

    def get_urls(self) -> list[URLPattern]:
        return [
            path(
                "<int:object_id>/view/",
                self.admin_site.admin_view(view_sent_email),
                name="view-sent-email",
            ),
        ] + super().get_urls()

    def get_view_on_site_url(self, obj) -> str | None:
        return reverse("admin:view-sent-email", args=(obj.id,))

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = None
    ) -> bool:
        return False
