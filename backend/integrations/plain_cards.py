from django.urls import reverse
from grants.models import Grant


def create_grant_card(request, user, conference):
    grant = Grant.objects.of_user(user).for_conference(conference).first()

    if not grant:
        return {"key": "grant", "components": []}

    admin_url = request.build_absolute_uri(
        reverse("admin:grants_grant_change", args=(grant.id,))
    )

    return {
        "key": "grant",
        "components": list(
            filter(
                None,
                [
                    {
                        "componentRow": {
                            "rowMainContent": [
                                {
                                    "componentText": {
                                        "textColor": "MUTED",
                                        "text": "Status",
                                    }
                                }
                            ],
                            "rowAsideContent": [
                                {
                                    "componentBadge": {
                                        "badgeLabel": grant.get_status_display(),
                                        "badgeColor": _grant_status_to_color(
                                            grant.status
                                        ),
                                    }
                                }
                            ],
                        }
                    },
                    {"componentSpacer": {"spacerSize": "M"}},
                    {
                        "componentRow": {
                            "rowMainContent": [
                                {
                                    "componentText": {
                                        "textColor": "MUTED",
                                        "text": "Approval type",
                                    }
                                }
                            ],
                            "rowAsideContent": [
                                {
                                    "componentText": {
                                        "textColor": "NORMAL",
                                        "text": (
                                            grant.get_approved_type_display()
                                            if grant.approved_type
                                            else "Empty"
                                        ),
                                    }
                                }
                            ],
                        }
                    },
                    {"componentSpacer": {"spacerSize": "M"}},
                    (
                        {
                            "componentRow": {
                                "rowMainContent": [
                                    {
                                        "componentText": {
                                            "textColor": "MUTED",
                                            "text": "Travel amount",
                                        }
                                    }
                                ],
                                "rowAsideContent": [
                                    {
                                        "componentText": {
                                            "textColor": "NORMAL",
                                            "text": f"€{grant.travel_amount}",
                                        }
                                    }
                                ],
                            }
                        }
                        if grant.has_approved_travel()
                        else None
                    ),
                    (
                        {"componentSpacer": {"spacerSize": "M"}}
                        if grant.has_approved_travel()
                        else None
                    ),
                    {
                        "componentRow": {
                            "rowMainContent": [
                                {
                                    "componentLinkButton": {
                                        "linkButtonLabel": "Open Grant in admin",
                                        "linkButtonUrl": admin_url,
                                    }
                                }
                            ],
                            "rowAsideContent": [],
                        }
                    },
                ],
            )
        ),
    }


def _grant_status_to_color(status):
    if status in (Grant.Status.approved, Grant.Status.confirmed):
        return "GREEN"
    elif status in (Grant.Status.waiting_for_confirmation):
        return "BLUE"
    elif status in (Grant.Status.waiting_list, Grant.Status.waiting_list_maybe):
        return "YELLOW"
    elif status in (Grant.Status.rejected, Grant.Status.refused):
        return "RED"

    return "GREY"
