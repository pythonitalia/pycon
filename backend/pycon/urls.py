from django.conf.urls import url, include
from django.contrib import admin

from graphene_django.views import GraphQLView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^graphql', GraphQLView.as_view(graphiql=True)),
    url('', include('social_django.urls', namespace='social')),
    url('user/', include('users.urls')),
]
