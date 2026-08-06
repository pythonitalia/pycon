from cross_inertia.django import render
from django.http import HttpRequest, HttpResponse


def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, "Dashboard")
