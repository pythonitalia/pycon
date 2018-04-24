from django.conf import settings
from django.urls import path

from .views import post_login_view

urlpatterns = [
    path('post-login', post_login_view, name='post-login'),
]

if settings.DEBUG:  # pragma: no cover
    from django.views.generic import TemplateView

    urlpatterns += [
        path('demo-login/',
             TemplateView.as_view(template_name='users/test-login.html')),
    ]
