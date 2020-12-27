from admin_views.admin import AdminViews
from conferences.models.conference import Conference
from django.contrib import admin, messages
from django.shortcuts import redirect
from newsletters.exporter import Endpoint
from notifications.aws import send_endpoints_to_pinpoint
from pretix import get_all_order_positions, get_items
from users.models import User

from .exporter import convert_user_to_endpoint
from .models import Subscription


def get_positions_with_missing_user(users, conference):
    admission_items = get_items(conference, {"admission": True})
    admission_items_ids = list(admission_items.keys())

    order_positions = [
        position
        for position in get_all_order_positions(
            conference,
            {"order__status": "p", "item__in": ",".join(admission_items_ids)},
        )
        if position["attendee_email"]
    ]

    position_by_email = {
        position["attendee_email"]: position for position in order_positions
    }

    order_emails = set(position_by_email)
    user_emails = set([user.email for user in users])

    missing_emails = order_emails - user_emails

    for email in missing_emails:
        yield position_by_email[email]


def get_missing_users_endpoints(users):
    conference = Conference.objects.last()
    positions = get_positions_with_missing_user(users, conference)

    return [
        Endpoint(
            id=f"pretix_{position['attendee_email']}",
            name=position["attendee_name"],
            full_name=position["attendee_name"],
            email=position["attendee_email"],
            is_staff=False,
            has_sent_submission_to=[],
            has_item_in_schedule=[],
            has_cancelled_talks=[],
            has_ticket=[conference.code],
            talks_by_conference={},
        )
        for position in positions
    ]


@admin.register(Subscription)
class SubscriptionAdmin(AdminViews):
    list_display = ("email", "date_subscribed")
    admin_views = (("Export all users to Pinpoint", "export_all_users_to_pinpoint"),)

    def export_all_users_to_pinpoint(self, request, **kwargs):
        users = User.objects.all()

        endpoints = [
            convert_user_to_endpoint(user) for user in users
        ] + get_missing_users_endpoints(users)

        send_endpoints_to_pinpoint(endpoints)

        self.message_user(
            request, "Exported all the users to Pinpoint", level=messages.SUCCESS
        )

        return redirect("admin:index")
