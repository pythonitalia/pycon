from datetime import UTC, date, datetime, time, timedelta

from cross_inertia.django import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, F, Sum
from django.db.models.functions import Coalesce
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme

from conferences.models import Conference, Deadline
from dashboard.pretix_analytics import load_pretix_ticket_analytics
from grants.models import Grant, GrantReimbursement
from submissions.models import Submission
from voting.models import Vote


def _get_next_url(request: HttpRequest) -> str:
    next_url = request.GET.get("next", "/dashboard")

    if next_url.startswith("/") and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url

    return "/dashboard"


def _frontend_url(path: str) -> str:
    return f"{settings.FRONTEND_URL.rstrip('/')}/{path.lstrip('/')}"


def _conference_data(conference: Conference) -> dict:
    return {
        "code": conference.code,
        "name": str(conference.name),
        "organizer": conference.organizer.name
        if conference.organizer
        else "Python Italia",
        "year": conference.start.year if conference.start else None,
    }


def _local_date(conference: Conference, value) -> date | None:
    if value is None:
        return None

    return timezone.localtime(value, timezone=conference.timezone).date()


def _count_label(count: int, singular: str, plural: str | None = None) -> str:
    label = singular if count == 1 else plural or f"{singular}s"
    return f"{count:,} {label}"


def _deadline_label(deadline: Deadline, today: date) -> str:
    start = _local_date(deadline.conference, deadline.start)
    end = _local_date(deadline.conference, deadline.end)

    if deadline.type == Deadline.TYPES.cfp:
        if end and end < today:
            return "CFP closed"
        if start and start <= today:
            return "CFP open"
        return "CFP opens"

    if deadline.type == Deadline.TYPES.voting:
        if end and end < today:
            return "Voting closed"
        if start and start <= today:
            return "Voting open"
        return "Voting opens"

    return str(deadline.name)


def _relative_label(value: date, today: date) -> str | None:
    days = (value - today).days

    if days == 0:
        return "Today"
    if days > 0:
        return f"In {days} day{'s' if days != 1 else ''}"

    return None


def _milestone_data(
    conference: Conference,
    today: date,
) -> list[dict]:
    proposal_count = conference.submissions.count()
    vote_count = Vote.objects.filter(submission__conference=conference).count()
    milestones = []

    for deadline in conference.deadlines.all():
        deadline_date = _local_date(conference, deadline.end)

        if deadline_date is None or deadline.type not in {
            Deadline.TYPES.cfp,
            Deadline.TYPES.voting,
            Deadline.TYPES.custom,
        }:
            continue

        metric = None
        if deadline.type == Deadline.TYPES.cfp:
            metric = _count_label(proposal_count, "proposal")
        elif deadline.type == Deadline.TYPES.voting:
            metric = _count_label(vote_count, "vote cast", "votes cast")

        milestones.append(
            {
                "date": deadline_date,
                "id": f"deadline-{deadline.pk}",
                "label": _deadline_label(deadline, today),
                "metric": metric,
            }
        )

    start_date = _local_date(conference, conference.start)
    if start_date:
        milestones.append(
            {
                "date": start_date,
                "id": "doors-open",
                "label": "Doors open",
                "metric": None,
            }
        )

    milestones.sort(key=lambda milestone: milestone["date"])
    current_index = next(
        (
            index
            for index, milestone in enumerate(milestones)
            if milestone["date"] >= today
        ),
        None,
    )

    return [
        {
            **milestone,
            "date": milestone["date"].isoformat(),
            "relative": _relative_label(milestone["date"], today)
            if index == current_index
            else None,
            "status": "complete"
            if milestone["date"] < today
            else "current"
            if index == current_index
            else "upcoming",
        }
        for index, milestone in enumerate(milestones)
    ]


def _weekly_counts(queryset, conference: Conference) -> list[dict]:
    today = timezone.localdate(timezone=conference.timezone)
    current_week = today - timedelta(days=today.weekday())
    first_week = current_week - timedelta(weeks=7)
    first_moment = datetime.combine(
        first_week,
        time.min,
        tzinfo=conference.timezone,
    ).astimezone(UTC)
    counts = [0] * 8

    for created in queryset.filter(created__gte=first_moment).values_list(
        "created", flat=True
    ):
        local_date = timezone.localtime(
            created,
            timezone=conference.timezone,
        ).date()
        week_index = (local_date - first_week).days // 7

        if 0 <= week_index < len(counts):
            counts[week_index] += 1

    weeks = []
    for index, count in enumerate(counts):
        week = first_week + timedelta(weeks=index)
        weeks.append(
            {
                "label": f"{week.strftime('%b')} {week.day}",
                "value": count,
            }
        )

    return weeks


def _status_breakdown(queryset, labels: dict[str, str]) -> list[dict]:
    counts = {
        item["effective_status"]: item["count"]
        for item in queryset.annotate(
            effective_status=Coalesce("pending_status", "status")
        )
        .values("effective_status")
        .annotate(count=Count("id"))
    }
    total = sum(counts.values())

    return [
        {
            "id": status,
            "label": label,
            "count": counts[status],
            "share": round((counts[status] / total) * 100) if total else 0,
        }
        for status, label in labels.items()
        if counts.get(status, 0) > 0
    ]


def _analytics_year(conference: Conference) -> int:
    if conference.start:
        return conference.start.year

    return timezone.localdate(timezone=conference.timezone).year


def _live_analytics_data(conference: Conference) -> list[dict]:
    year = _analytics_year(conference)
    proposal_queryset = Submission.objects.filter(conference=conference)
    grant_queryset = Grant.objects.filter(conference=conference)
    proposals = _weekly_counts(proposal_queryset, conference)
    grants = _weekly_counts(grant_queryset, conference)
    proposal_total = proposal_queryset.count()
    grant_total = grant_queryset.count()
    proposal_breakdown = _status_breakdown(
        proposal_queryset,
        {
            Submission.STATUS.proposed: "Awaiting review",
            Submission.STATUS.accepted: "Accepted",
            Submission.STATUS.waiting_list: "Waiting list",
            Submission.STATUS.rejected: "Declined by us",
            Submission.STATUS.cancelled: "Withdrawn by speaker",
        },
    )
    grant_breakdown = _status_breakdown(
        grant_queryset,
        {
            Grant.Status.pending: "Awaiting review",
            Grant.Status.approved: "Approved",
            Grant.Status.waiting_for_confirmation: "Awaiting grantee confirmation",
            Grant.Status.confirmed: "Confirmed",
            Grant.Status.waiting_list: "Waiting list",
            Grant.Status.waiting_list_maybe: "Waiting list, maybe",
            Grant.Status.refused: "Declined by grantee",
            Grant.Status.rejected: "Declined by us",
            Grant.Status.did_not_attend: "Did not attend",
        },
    )
    allocated_total = (
        GrantReimbursement.objects.filter(grant__conference=conference)
        .annotate(effective_status=Coalesce("grant__pending_status", "grant__status"))
        .filter(
            effective_status__in=[
                Grant.Status.approved,
                Grant.Status.waiting_for_confirmation,
                Grant.Status.confirmed,
            ]
        )
        .aggregate(total=Sum("granted_amount"))["total"]
        or 0
    )

    return [
        load_pretix_ticket_analytics(conference),
        {
            "id": "proposals-received",
            "title": "Proposals received",
            "period": "Last 8 weeks",
            "summary": "submitted · all time",
            "total": proposal_total,
            "values": proposals,
            "comparisonValues": [],
            "currentLabel": f"{year} cumulative",
            "comparisonLabel": f"{year - 1}, same period",
            "annotations": [],
            "comparisonAnnotations": [],
            "breakdown": proposal_breakdown,
            "comparisonBreakdown": [],
            "products": [],
            "details": [],
            "allocatedTotal": None,
        },
        {
            "id": "grants-received",
            "title": "Grants received",
            "period": "All time",
            "summary": "requests received",
            "total": grant_total,
            "values": grants,
            "comparisonValues": [],
            "currentLabel": f"{year} requests",
            "comparisonLabel": f"{year - 1}, same period",
            "annotations": [],
            "comparisonAnnotations": [],
            "breakdown": grant_breakdown,
            "comparisonBreakdown": [],
            "products": [],
            "details": [],
            "allocatedTotal": int(allocated_total),
        },
    ]


def _selected_conference_data(conference: Conference) -> dict:
    start_date = _local_date(conference, conference.start)
    end_date = _local_date(conference, conference.end)
    today = timezone.localdate(timezone=conference.timezone)

    if start_date is None:
        countdown = {"label": "dates not set", "value": "—"}
    elif today < start_date:
        countdown = {
            "label": "days to doors",
            "value": str((start_date - today).days),
        }
    elif end_date and today <= end_date:
        countdown = {"label": "conference underway", "value": "Live"}
    else:
        countdown = {"label": "conference complete", "value": "Ended"}

    return {
        **_conference_data(conference),
        "analytics": _live_analytics_data(conference),
        "countdown": countdown,
        "endDate": end_date.isoformat() if end_date else None,
        "location": conference.location,
        "milestones": _milestone_data(conference, today),
        "startDate": start_date.isoformat() if start_date else None,
    }


def _render_dashboard(
    request: HttpRequest,
    conferences: list[Conference],
    selected_conference: Conference | None,
) -> HttpResponse:
    user = request.user
    comparison_codes = {
        code
        for value in request.GET.getlist("compare")
        for code in value.split(",")
        if code
    }
    max_comparison_conferences = max(
        0,
        settings.DASHBOARD_MAX_COMPARISON_CONFERENCES,
    )
    comparison_conferences = [
        conference
        for conference in conferences
        if conference.code in comparison_codes
        and conference.code != getattr(selected_conference, "code", None)
    ][:max_comparison_conferences]

    return render(
        request,
        "Dashboard",
        {
            "user": {
                "name": user.display_name or user.email,
                "email": user.email,
                "avatar": None,
                "profileUrl": _frontend_url("/profile"),
            },
            "conferences": [_conference_data(conference) for conference in conferences],
            "maxComparisonConferences": max_comparison_conferences,
            "comparisonConferences": [
                _selected_conference_data(conference)
                for conference in comparison_conferences
            ],
            "selectedConference": _selected_conference_data(selected_conference)
            if selected_conference
            else None,
        },
    )


def _conferences() -> list[Conference]:
    return list(
        Conference.objects.select_related("organizer")
        .prefetch_related("deadlines")
        .order_by(F("start").desc(nulls_last=True), "code")
    )


def _require_dashboard_access(request: HttpRequest) -> None:
    if settings.DASHBOARD_REQUIRE_STAFF and not request.user.is_staff:
        raise PermissionDenied


@login_required(login_url="dashboard-login")
def dashboard_index(request: HttpRequest) -> HttpResponse:
    _require_dashboard_access(request)
    conferences = _conferences()

    if conferences:
        return redirect("dashboard-conference", conference_code=conferences[0].code)

    return _render_dashboard(request, conferences, None)


@login_required(login_url="dashboard-login")
def dashboard(request: HttpRequest, conference_code: str) -> HttpResponse:
    _require_dashboard_access(request)
    conferences = _conferences()
    selected_conference = next(
        (
            conference
            for conference in conferences
            if conference.code == conference_code
        ),
        None,
    )

    if selected_conference is None:
        raise Http404

    return _render_dashboard(request, conferences, selected_conference)


def login(request: HttpRequest) -> HttpResponse:
    next_url = _get_next_url(request)

    if request.user.is_authenticated:
        return redirect(next_url)

    return render(
        request,
        "Login",
        {
            "nextUrl": next_url,
            "privacyPolicyUrl": _frontend_url("/privacy-policy"),
            "resetPasswordUrl": _frontend_url("/reset-password"),
        },
    )
