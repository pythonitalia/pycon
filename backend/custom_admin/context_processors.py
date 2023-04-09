from django.conf import settings


def admin_settings(request):
    return {"CURRENT_ENV": settings.ENVIRONMENT}


def astro_settings(request):
    return {
        "ASTRO_URL": "http://localhost:3002",
        "GATEWAY_GRAPHQL_URL": f"{settings.GATEWAY_SERVICE}/graphql",
    }
