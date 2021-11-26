from django.conf import settings


def admin_settings(request):
    return {"CURRENT_ENV": settings.ENV}
