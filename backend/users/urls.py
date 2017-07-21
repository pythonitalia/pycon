from django.conf import settings
from django.conf.urls import url

from .views import post_login_view

urlpatterns = [
    url(r'post-login', post_login_view, name='post-login'),
]

if settings.DEBUG:
    from django.views.generic import TemplateView

    urlpatterns += [
        url(r'demo-login/',
            TemplateView.as_view(template_name='users/test-login.html')),
    ]
