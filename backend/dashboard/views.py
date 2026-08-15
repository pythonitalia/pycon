from cross_inertia.django import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme


def _get_next_url(request: HttpRequest) -> str:
    next_url = request.GET.get("next", "/dashboard")

    if next_url.startswith("/") and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url

    return "/dashboard"


@login_required(login_url="dashboard-login")
def dashboard(request: HttpRequest) -> HttpResponse:
    user = request.user

    return render(
        request,
        "Dashboard",
        {
            "user": {
                "name": user.display_name or user.email,
                "email": user.email,
                "avatar": None,
            }
        },
    )


def login(request: HttpRequest) -> HttpResponse:
    next_url = _get_next_url(request)

    if request.user.is_authenticated:
        return redirect(next_url)

    return render(request, "Login", {"nextUrl": next_url})
