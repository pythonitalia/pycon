from django.urls import path

from association_membership.views import pretix_webhook, stripe_webhook


urlpatterns = [
    path("stripe-webhook/", stripe_webhook, name="stripe-webhook"),
    path("pretix-webhook/", pretix_webhook, name="pretix-webhook"),
]
