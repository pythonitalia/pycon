from django.conf import settings
from django.http import JsonResponse
from users.models import User


def healthcheck(request):
    User.objects.exists()

    return JsonResponse(
        {
            "status": "ok",
            "version": settings.GITHASH,
        }
    )
