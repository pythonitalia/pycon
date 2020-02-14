from collections import defaultdict

from admin_views.admin import AdminViews
from django.contrib import admin, messages
from django.shortcuts import redirect
from notifications.aws import (
    Endpoint,
    convert_users_to_endpoints,
    send_endpoints_to_pinpoint,
)
from schedule.models import ScheduleItem
from users.models import User

from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(AdminViews):
    list_display = ("email", "date_subscribed")
    admin_views = (
        ("Export all users to Pinpoint", "export_all_users_to_pinpoint"),
        ("Export users with accepted talks", "export_users_with_accepted_talks"),
    )

    def export_all_users_to_pinpoint(self, request, **kwargs):
        users = User.objects.all()

        endpoints = convert_users_to_endpoints(users)
        send_endpoints_to_pinpoint(endpoints)

        self.message_user(
            request, "Exported all the users to Pinpoint", level=messages.SUCCESS
        )

        return redirect("admin:index")

    def export_users_with_accepted_talks(self, request, **kwargs):
        items = ScheduleItem.objects.filter(
            type__in=[
                ScheduleItem.TYPES.keynote,
                ScheduleItem.TYPES.training,
                ScheduleItem.TYPES.submission,
            ]
        )

        items_by_user = defaultdict(list)
        users = {}

        for item in items:
            for user in item.speakers:
                users[user.id] = user
                items_by_user[user.id].append(item)

        endpoints = []

        for id, user in users.items():
            items_by_conference = defaultdict(list)
            user_items = items_by_user[id]

            for item in user_items:
                items_by_conference[item.slot.day.conference.code].append(item.title)

            endpoints.append(
                Endpoint(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    full_name=user.full_name,
                    is_staff=user.is_staff,
                    extra_info={
                        "has_item_in_schedule": list(items_by_conference.keys()),
                        **{
                            f"{key}_items_in_schedule": value
                            for key, value in items_by_conference.items()
                        },
                    },
                )
            )

        send_endpoints_to_pinpoint(endpoints)

        self.message_user(
            request,
            "Exported all the users with items in schedule to Pinpoint",
            level=messages.SUCCESS,
        )

        return redirect("admin:index")
