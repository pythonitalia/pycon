"""Custom Django admin index (landing page).

Overrides ``admin.site.index`` to render a dashboard that organizes the
registered models into workflow groups and exposes a few quick-action
shortcuts, instead of the stock alphabetical app/model table.

The grouping is driven by ``GROUPS`` below (keyed by model ``object_name``).
Any registered model not listed falls through to an "Other" group, so no model
is ever silently dropped -- a test enforces this.
"""

from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import NoReverseMatch, reverse

INDEX_TEMPLATE = "astro/landing.html"

# Ordered workflow groups. Keys are group titles; values are the model
# ``object_name``s that belong to each group. Order here is the display order.
GROUPS: dict[str, list[str]] = {
    "Program": [
        "Submission",
        "SubmissionType",
        "SubmissionTag",
        "SubmissionComment",
        "SubmissionConfirmPendingStatusProxy",
        "Vote",
        "RankSubmission",
        "RankRequest",
        "RankStat",
        "UserReview",
        "ReviewSession",
        "Keynote",
        "Event",
    ],
    "Schedule & Video": [
        "ScheduleItem",
        "ScheduleItemInvitation",
        "Room",
        "Day",
        "ScheduleItemSentForVideoUpload",
        "WetransferToS3TransferRequest",
    ],
    "Finance": [
        "Grant",
        "GrantReimbursement",
        "GrantReimbursementCategory",
        "GrantConfirmPendingStatusProxy",
        "Invoice",
        "Sender",
        "Address",
        "Item",
        "BillingAddress",
        "PretixPayment",
        "StripeSubscriptionPayment",
        "Membership",
    ],
    "Sponsors": [
        "Sponsor",
        "SponsorBenefit",
        "SponsorLevel",
        "SponsorSpecialOption",
        "SponsorLead",
    ],
    "People": [
        "User",
        "Participant",
        "AttendeeConferenceRole",
        "BadgeScan",
        "InvitationLetterRequest",
        "InvitationLetterConferenceConfig",
        "Organizer",
        "Notification",
        "VolunteerDevice",
    ],
    "Conference setup": [
        "Conference",
        "Topic",
        "AudienceLevel",
        "Deadline",
        "ConferenceVoucher",
        "ChecklistItem",
        "Language",
    ],
    "Content & CMS": [
        "Post",
        "Page",
        "GenericCopy",
        "FAQ",
        "Menu",
        "MenuLink",
        "JobListing",
        "Subscription",
    ],
    "Comms": [
        "EmailTemplate",
        "SentEmail",
    ],
    "System": [
        "APIToken",
        "GoogleCloudOAuthCredential",
        "File",
    ],
}

OTHER_GROUP = "Other"


def _model_to_group() -> dict[str, str]:
    """Reverse map: model object_name -> group title."""
    mapping = {}
    for group, object_names in GROUPS.items():
        for object_name in object_names:
            mapping[object_name] = group
    return mapping


def _clean_model(model: dict, app: dict) -> dict:
    """Produce a JSON-serializable model entry from Django's app_list dict.

    Django's raw model dict carries the model class and lazy strings, neither of
    which survive json.dumps -- so pick only the fields the frontend needs and
    coerce names to plain strings.
    """
    return {
        "name": str(model["name"]),
        "object_name": model["object_name"],
        "admin_url": model.get("admin_url"),
        "add_url": model.get("add_url"),
        "view_only": model.get("view_only", False),
        "app_label": app["app_label"],
        "app_name": str(app["name"]),
    }


def build_groups(app_list: list[dict]) -> list[dict]:
    """Bucket the models from Django's ``app_list`` into workflow groups.

    Returns an ordered list of ``{"title", "models"}`` dicts with serializable
    model entries. Empty groups are omitted. Any model whose ``object_name``
    isn't mapped lands in the Other group, so nothing is silently dropped.
    """
    model_to_group = _model_to_group()
    buckets: dict[str, list[dict]] = {title: [] for title in GROUPS}
    buckets[OTHER_GROUP] = []

    for app in app_list:
        for model in app["models"]:
            group = model_to_group.get(model["object_name"], OTHER_GROUP)
            buckets[group].append(_clean_model(model, app))

    ordered_titles = [*GROUPS.keys(), OTHER_GROUP]
    return [
        {"title": title, "models": buckets[title]}
        for title in ordered_titles
        if buckets[title]
    ]


def build_all_apps(app_list: list[dict]) -> list[dict]:
    """Serializable copy of Django's full app/model list (the fallback section)."""
    return [
        {
            "app_label": app["app_label"],
            "name": str(app["name"]),
            "models": [_clean_model(model, app) for model in app["models"]],
        }
        for app in app_list
    ]


def build_quick_links(request) -> list[dict]:
    """Curated shortcuts to common daily tasks.

    Each link is ``{"title", "description", "url"}``. Links whose target can't
    be resolved (e.g. a feature not wired in this deploy) are skipped.
    """
    links = []

    # Schedule builder is per-conference; point at the most recent conference,
    # falling back to the conference changelist.
    schedule_url = _latest_schedule_builder_url() or _safe_reverse(
        "admin:conferences_conference_changelist"
    )
    if schedule_url:
        links.append(
            {
                "title": "Schedule builder",
                "description": "Build the conference schedule",
                "url": schedule_url,
            }
        )

    grants_url = _safe_reverse("admin:grants_grant_changelist")
    if grants_url:
        links.append(
            {
                "title": "Review grants",
                "description": "Review and update grant requests",
                "url": grants_url,
            }
        )

    submissions_url = _safe_reverse("admin:submissions_submission_changelist")
    if submissions_url:
        links.append(
            {
                "title": "Review submissions",
                "description": "Review proposed talks",
                "url": submissions_url,
            }
        )

    return links


def _safe_reverse(viewname, **kwargs):
    try:
        return reverse(viewname, **kwargs)
    except NoReverseMatch:
        return None


def _latest_schedule_builder_url():
    from conferences.models import Conference

    conference = Conference.objects.order_by("-start").first()
    if conference is None:
        return None
    return _safe_reverse("admin:schedule_builder", kwargs={"object_id": conference.pk})


def custom_index(request, extra_context=None):
    """Render the dashboard landing page in place of the stock admin index."""
    app_list = admin.site.get_app_list(request)
    context = {
        **admin.site.each_context(request),
        "title": admin.site.index_title,
        "app_list": app_list,
        "groups": build_groups(app_list),
        "all_apps": build_all_apps(app_list),
        "quick_links": build_quick_links(request),
        "breadcrumbs": [],
        **(extra_context or {}),
    }
    request.current_app = admin.site.name
    return TemplateResponse(request, INDEX_TEMPLATE, context)


def install():
    """Replace the default admin site's index view with ``custom_index``."""
    admin.site.index = custom_index
