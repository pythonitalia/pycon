from django.conf import settings


def admin_settings(request):
    return {"CURRENT_ENV": settings.ENVIRONMENT}


def astro_settings(request):
    return {
        "ASTRO_URL": request.build_absolute_uri("/astro"),
        "APOLLO_GRAPHQL_URL": "/admin/graphql",
    }
