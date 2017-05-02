from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib import admin

from graphene_django.views import GraphQLView

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls


urlpatterns = [
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^django-admin/', admin.site.urls),

    url(r'^graphql', GraphQLView.as_view(graphiql=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
