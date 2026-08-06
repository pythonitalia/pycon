from cross_inertia.django import render
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme

from conferences.models import Conference


def _get_next_url(request: HttpRequest) -> str:
    next_url = request.GET.get("next", "/dashboard")

    if next_url.startswith("/") and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url

    return "/dashboard"


def _conference_data(conference: Conference) -> dict:
    return {
        "code": conference.code,
        "name": str(conference.name),
        "organizer": conference.organizer.name
        if conference.organizer
        else "Python Italia",
        "year": conference.start.year if conference.start else None,
    }


def _render_dashboard(
    request: HttpRequest,
    conferences: list[Conference],
    selected_conference: Conference | None,
) -> HttpResponse:
    user = request.user

    return render(
        request,
        "Dashboard",
        {
            "user": {
                "name": user.display_name or user.email,
                "email": user.email,
                "avatar": None,
            },
            "conferences": [_conference_data(conference) for conference in conferences],
            "selectedConference": _conference_data(selected_conference)
            if selected_conference
            else None,
        },
    )


def _conferences() -> list[Conference]:
    return list(
        Conference.objects.select_related("organizer").order_by(
            F("start").desc(nulls_last=True), "code"
        )
    )


@login_required(login_url="dashboard-login")
def dashboard_index(request: HttpRequest) -> HttpResponse:
    conferences = _conferences()

    if conferences:
        return redirect("dashboard-conference", conference_code=conferences[0].code)

    return _render_dashboard(request, conferences, None)


@login_required(login_url="dashboard-login")
def dashboard(request: HttpRequest, conference_code: str) -> HttpResponse:
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

    return render(request, "Login", {"nextUrl": next_url})
