import os
from django.conf import settings
from django.http import JsonResponse
from users.models import User


def healthcheck(request):
    if os.path.exists("shutdown"):
        return JsonResponse(
            {
                "status": "shutdown",
                "version": settings.GITHASH,
            },
            status=503,
        )

    User.objects.exists()

    return JsonResponse(
        {
            "status": "ok",
            "version": settings.GITHASH,
        }
    )
