from django.utils import timezone
from django.contrib.admin.options import IS_POPUP_VAR
from django.db import transaction
from typing import Any
from django.contrib import admin, messages

from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from users.models import User
from schedule.tasks import (
    calculate_recipients_for_email_speaker,
    process_email_speaker_for_sending,
)
from email_speakers.models import EmailSpeaker, EmailSpeakerRecipient
from django import forms
from django.utils.safestring import mark_safe


class EmailSpeakerForm(forms.ModelForm):
    test_email = forms.EmailField(required=False)

    class Meta:
        model = EmailSpeaker
        exclude = ()


class EmailSpeakerRecipientInline(admin.TabularInline):
    model = EmailSpeakerRecipient
    extra = 0
    readonly_fields = (
        "status",
        "user",
        "sent_at",
    )
    fields = (
        "status",
        "user",
        "sent_at",
    )
    show_change_link = True
    can_delete = False
    verbose_name = "Recipient"
    verbose_name_plural = "Recipients"

    def has_add_permission(self, request: HttpRequest, obj) -> bool:
        return False

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).filter(is_test=False)


@admin.register(EmailSpeaker)
class EmailSpeakerAdmin(admin.ModelAdmin):
    form = EmailSpeakerForm
    list_display = ("subject", "status", "conference")
    search_fields = ("conference", "subject", "body")
    list_filter = (
        "status",
        "conference",
        "sent_at",
    )
    readonly_fields = (
        "created",
        "modified",
        "status",
        "send_test_email",
        "send_email_to_speakers",
        "sent_at",
        "conference",
        "show_recipients",
    )
    inlines = [EmailSpeakerRecipientInline]
    date_hierarchy = "created"

    def changeform_view(
        self,
        request: HttpRequest,
        object_id: str,
        form_url: str = ...,
        extra_context: dict[str, bool] | None = ...,
    ) -> HttpResponse:
        extra_context = extra_context or {}
        extra_context.update(
            {
                "show_save_and_add_another": False,
                "show_save_and_continue": True,
                "show_save": False,
            }
        )
        return super().changeform_view(request, object_id, form_url, extra_context)

    def get_inlines(self, request: HttpRequest, obj: Any | None):
        return super().get_inlines(request, obj) if obj else []

    def get_readonly_fields(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> list[str] | tuple[Any, ...]:
        readyonly_fields = super().get_readonly_fields(request, obj)

        if not obj:
            return set(readyonly_fields) - {
                "conference",
            }

        return readyonly_fields

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = None
    ) -> bool:
        if obj and obj.status != EmailSpeaker.Status.draft:
            return False
        return super().has_change_permission(request, obj)

    def response_add(self, request, obj, post_url_continue=None):
        if "_addanother" not in request.POST and IS_POPUP_VAR not in request.POST:
            request.POST = request.POST.copy()
            request.POST["_continue"] = 1
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if (
            "_send_test_email" in request.POST
            or "_send_email_to_speakers" in request.POST
            or "_show_recipients" in request.POST
        ):
            request.POST = request.POST.copy()
            request.POST["_continue"] = 1

        return super().response_change(request, obj)

    def save_form(self, request: Any, form: Any, change: Any) -> Any:
        instance = super().save_form(request, form, change)

        if "_send_test_email" in form.data:
            test_email = form.cleaned_data.get("test_email")
            if not test_email:
                self.message_user(
                    request,
                    "No test email specified.",
                    messages.ERROR,
                )
                return instance

            user = User.objects.filter(email=test_email).first()

            if not user:
                self.message_user(
                    request,
                    f"No user found with email {test_email}.",
                    messages.ERROR,
                )
                return instance

            transaction.on_commit(
                lambda: process_email_speaker_for_sending.delay(
                    email_speaker_id=instance.id,
                    recipient_user_id=user.id,
                    is_test=True,
                )
            )

            self.message_user(
                request,
                f"Test email sent to {user.email}.",
                messages.SUCCESS,
            )

        if "_send_email_to_speakers" in form.data:
            instance.sent_at = timezone.now()
            instance.status = EmailSpeaker.Status.in_progress
            instance.save(update_fields=["sent_at", "status"])

            transaction.on_commit(
                lambda: process_email_speaker_for_sending.delay(
                    email_speaker_id=instance.id, is_test=False
                )
            )

            self.message_user(
                request,
                "Sending the email.",
                messages.SUCCESS,
            )

        if "_show_recipients" in form.data:
            transaction.on_commit(
                lambda: calculate_recipients_for_email_speaker.delay(
                    email_speaker_id=instance.id,
                    status=EmailSpeakerRecipient.Status.draft,
                )
            )
            self.message_user(
                request,
                "Calculating recipients in background.",
                messages.INFO,
            )

        return instance

    def send_email_to_speakers(self, obj):
        return mark_safe(
            """
            <input type="submit" name="_send_email_to_speakers" value="Send email to speakers!" style="background-color: var(--delete-button-bg)" />
        """
        )

    def send_test_email(self, obj):
        return mark_safe(
            """
            <input type="submit" name="_send_test_email" value="Send test email" />
        """
        )

    def show_recipients(self, obj):
        if not obj.is_draft:
            return None
        return mark_safe(
            """
            <input type="submit" name="_show_recipients" value="Show recipients" />
        """
        )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        if not obj:
            return [
                (
                    None,
                    {
                        "fields": (
                            "conference",
                            "subject",
                        )
                    },
                ),
            ]

        fieldsets = [
            (
                "Email",
                {
                    "fields": ("status", "conference", "subject", "body"),
                },
            ),
            (
                "Test email",
                {
                    "fields": ("test_email", "send_test_email"),
                },
            ),
            (
                "Recipients",
                {"fields": ("send_only_to_speakers_without_ticket", "show_recipients")},
            ),
            (
                "Send",
                {
                    "fields": ("send_email_to_speakers",),
                },
            ),
            (
                "Dates",
                {
                    "fields": ("sent_at", "created", "modified"),
                    "classes": ("collapse",),
                },
            ),
        ]

        if not obj.is_draft:
            fieldsets.pop(1)
            fieldsets.pop(2)
            fieldsets[-1][1]["classes"] = ()

        return fieldsets
