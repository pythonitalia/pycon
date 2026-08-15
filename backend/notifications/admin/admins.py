import functools
import logging
from django.db import transaction
from django.utils import timezone
from typing import Any
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.urls import reverse
from django.contrib import admin
from django.urls.resolvers import URLPattern
from custom_admin.widgets import RichEditorWidget
from notifications.admin.views import (
    view_sent_email,
    view_email_template,
)
from users.admin_mixins import ConferencePermissionMixin
from django.urls import path
from django.utils.safestring import mark_safe

from notifications.models import EmailTemplate, SentEmail, SentEmailEvent
from django.forms import Textarea
from django.db.models import QuerySet
from notifications.tasks import send_pending_email

logger = logging.getLogger(__name__)


class SentEmailEventInline(admin.TabularInline):
    model = SentEmailEvent
    extra = 0
    fields = ["event", "timestamp", "payload"]
    readonly_fields = ["event", "timestamp", "payload"]
    ordering = ["-timestamp"]
    show_change_link = False
    verbose_name = "Event"
    verbose_name_plural = "Events"


@admin.register(EmailTemplate)
class EmailTemplateAdmin(ConferencePermissionMixin, admin.ModelAdmin):
    list_display = ["identifier", "name", "conference"]
    list_filter = ["identifier", "conference"]
    fields = [
        "conference",
        "is_system_template",
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
            kwargs["widget"] = RichEditorWidget()

        if db_field.name in ("subject", "preview_text"):
            kwargs["widget"] = Textarea(attrs={"rows": 2, "cols": 200})

        return super().formfield_for_dbfield(db_field, **kwargs)

    def get_readonly_fields(self, request: HttpRequest, obj: Any | None = None):
        fields = super().get_readonly_fields(request, obj)

        if obj:
            fields = fields + ["conference", "is_system_template", "identifier"]

        return fields

    def response_post_save_add(self, request, obj):
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
                "<int:object_id>/view/",
                self.admin_site.admin_view(view_email_template),
                name="view-email-template",
            ),
        ] + super().get_urls()

    def get_view_on_site_url(self, obj) -> str | None:
        if not obj:
            return

        return reverse("admin:view-email-template", args=(obj.id,))


def _submit_emails_for_sending(sent_emails_ids: list[int]) -> None:
    for sent_email_id in sent_emails_ids:
        try:
            send_pending_email.delay(sent_email_id)
        except Exception:
            logger.exception(
                "Could not queue sent_email_id=%s, leaving it pending",
                sent_email_id,
            )


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
        "from_email",
        "subject",
        "preview_text",
        "placeholders",
        "reply_to",
        "cc_addresses",
        "bcc_addresses",
        "email_template",
        "is_delivered",
        "is_bounced",
        "is_opened",
        "is_complained",
    ]
    date_hierarchy = "sent_at"
    ordering = ["-sent_at"]
    autocomplete_fields = ["recipient"]
    inlines = [SentEmailEventInline]
    actions = ["send_email"]

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
        if not obj:
            return None

        return reverse("admin:view-sent-email", args=(obj.id,))

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = None
    ) -> bool:
        return False

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def get_queryset(self, request: HttpRequest) -> Any:
        qs = super().get_queryset(request).prefetch_related("email_template")

        if not request.user.is_superuser:
            qs = qs.filter(email_template__is_system_template=False)

        return qs

    @transaction.atomic
    def send_email(self, request: HttpRequest, queryset: QuerySet[SentEmail]):
        affected_emails_ids = list(
            queryset.filter(
                status__in=[
                    SentEmail.Status.draft,
                    SentEmail.Status.pending,
                    SentEmail.Status.failed,
                ]
            )
            .select_for_update(skip_locked=True)
            .values_list("id", flat=True)
        )

        SentEmail.objects.filter(id__in=affected_emails_ids).update(
            status=SentEmail.Status.pending,
            modified=timezone.now(),
        )

        transaction.on_commit(
            functools.partial(_submit_emails_for_sending, affected_emails_ids)
        )
        self.message_user(
            request, f"Emails queued for sending: {len(affected_emails_ids)}"
        )
