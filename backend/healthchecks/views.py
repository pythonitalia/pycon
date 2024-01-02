from users.models import User
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
)
from django.core.cache import cache
from django.conf import settings


@api_view(["GET"])
def health(request):
    status = {}

    try:
        User.objects.exists()
        status["db"] = True
    except Exception:
        status["db"] = False

    try:
        cache.set("_healthcheck", "1", timeout=2)
        status["cache"] = cache.get("_healthcheck") == "1"
    except Exception:
        status["cache"] = False

    status["version"] = settings.GITHASH
    return Response(status)
