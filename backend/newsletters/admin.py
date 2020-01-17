import typing
from dataclasses import dataclass

from admin_views.admin import AdminViews
from django.conf.urls import url
from django.contrib import admin, messages
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.html import format_html
from users.models import User

from .aws import create_cfp_segment, get_segment_names, send_users_to_pinpoint
from .models import Email, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(AdminViews):
    list_display = ("email", "date_subscribed")
    admin_views = (
        (
            "Export people that have sent proposal to Pinpoint",
            "export_people_that_have_sent_proposal",
        ),
    )

    def export_people_that_have_sent_proposal(
        self, *args, **kwargs
    ):  # pragma: no cover
        users = (
            User.objects.filter(submissions__isnull=False)
            .values(
                "id", "email", "name", conference=F("submissions__conference__code")
            )
            .distinct()
        )

        users_by_id = {}

        @dataclass
        class CFPUser:
            id: str
            name: str
            email: str
            submission_sent_to: typing.List[str]

        conferences = set()

        for user in users:
            user_id = str(user["id"])
            conference = user["conference"]

            conferences.add(conference)

            if user_id in users_by_id:
                users_by_id[user_id].submission_sent_to.append(conference)
            else:
                users_by_id[user_id] = CFPUser(
                    id=user_id,
                    name=user["name"],
                    email=user["email"],
                    submission_sent_to=[conference],
                )

        available_segments = get_segment_names()

        for conference in conferences:
            segment_name = f"{conference}-users-that-have-sent-a-proposal"

            if segment_name not in available_segments:
                create_cfp_segment(segment_name, conference)

        send_users_to_pinpoint(users_by_id.values())

        data = {"subscribers": None}

        return JsonResponse(data, status=200)


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    ordering = ["status", "scheduled_date", "-pk"]
    list_display = (
        "subject",
        "recipients_type",
        "scheduled_date",
        "status",
        "email_actions",
    )
    readonly_fields = ("recipients", "email_actions")
    actions = ["send_emails"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r"^(?P<email_id>.+)/send_email/$",
                self.admin_site.admin_view(self.send_email),
                name="send_email",
            )
        ]
        return custom_urls + urls

    def email_actions(self, obj):  # pragma: no cover
        if obj.status != Email.STATUS.sent:
            return format_html(
                '<a class="button" href="{}">Send Now!!</a>&nbsp;',
                reverse("admin:send_email", args=[obj.pk]),
            )
        return ""

    email_actions.short_description = "Email Actions"
    email_actions.allow_tags = True

    def send_email(self, request, email_id):
        self._send_emails(request, [Email.objects.get(pk=email_id)])
        return HttpResponseRedirect(reverse("admin:newsletters_email_changelist"))

    def send_emails(self, request, queryset):
        self._send_emails(request, queryset)

    def _send_emails(self, request, emails):

        results = []
        for email in emails:
            results.append(email.send_email())

        if all(results):
            subjects = "', '".join([e.subject for e in emails])
            self.message_user(request, f"Successfully sent '{subjects}' Email(s).")
        else:
            self.message_user(
                request, "Mmmm... Something went wrong :(", level=messages.ERROR
            )

    send_emails.short_description = "Send selected Emails"
