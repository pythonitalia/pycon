"""Bootstrap and maintain the dashboard-only data in local Pretix.

This file is executed through ``pretix shell`` by scripts/seed-dashboard-stage.
It intentionally knows nothing about production credentials or event identifiers.
"""

import os

from django.utils.dateparse import parse_datetime
from django_scopes import scopes_disabled
from pretix.base.models import Event, Organizer, Order, Team, TeamAPIToken, User

ACTION = os.environ.get("DASHBOARD_SEED_ACTION", "reset")
EVENT_SLUG = "dashboard-local"
ORGANIZER_SLUG = "python-italia-local"
TOKEN = os.environ.get("PYCON_LOCAL_PRETIX_TOKEN", "local-dashboard-api-token")


def bootstrap_access() -> Organizer:
    organizer, _ = Organizer.objects.get_or_create(
        slug=ORGANIZER_SLUG,
        defaults={"name": "Python Italia local"},
    )
    organizer.enable_plugin("pretix.plugins.banktransfer")
    organizer.save()

    user, _ = User.objects.get_or_create(
        email="admin@localhost",
        defaults={"fullname": "Local Pretix admin"},
    )
    user.fullname = "Local Pretix admin"
    user.is_active = True
    user.is_staff = True
    user.is_verified = True
    user.needs_password_change = False
    user.set_password("admin")
    user.save()

    permissions = {
        field.name: True
        for field in Team._meta.fields
        if field.name.startswith("can_")
    }
    team, _ = Team.objects.update_or_create(
        organizer=organizer,
        name="Local dashboard development",
        defaults={"all_events": True, **permissions},
    )
    team.members.add(user)
    TeamAPIToken.objects.update_or_create(
        team=team,
        name="Local dashboard seeder",
        defaults={"active": True, "token": TOKEN},
    )
    return organizer


def reset_event(organizer: Organizer) -> None:
    with scopes_disabled():
        event = Event.objects.filter(
            organizer=organizer,
            slug=EVENT_SLUG,
        ).first()
        if event is None:
            print("Local Pretix access is ready; there was no seeded event to reset.")
            return

        orders = list(Order.objects.filter(event=event))
        for order in orders:
            Order.objects.filter(pk=order.pk).update(testmode=True)
            order.testmode = True
            order.gracefully_delete()

        event.delete_sub_objects()
        event.delete()
        print(f"Reset local Pretix event and {len(orders)} orders.")


def apply_order_dates(organizer: Organizer) -> None:
    updated = 0
    with scopes_disabled():
        event = Event.objects.get(organizer=organizer, slug=EVENT_SLUG)
        orders = Order.objects.filter(event=event)
        for order in orders:
            ordered_at = parse_datetime(
                order.api_meta.get("dashboard_seed_ordered_at", "")
            )
            if ordered_at is None:
                continue
            Order.objects.filter(pk=order.pk).update(datetime=ordered_at)
            updated += 1

        event.settings.payment_banktransfer__enabled = True
        event.settings.payment_banktransfer_bank_details = "Local development only"
        event.clean_live()
        event.live = True
        event.save(update_fields=["live"])

    print(
        f"Applied historical timestamps to {updated} local Pretix orders and "
        "published the local event."
    )


organizer = bootstrap_access()
if ACTION == "reset":
    reset_event(organizer)
elif ACTION == "apply-order-dates":
    apply_order_dates(organizer)
else:
    raise ValueError(f"Unknown DASHBOARD_SEED_ACTION: {ACTION}")
