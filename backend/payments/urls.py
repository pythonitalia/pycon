from django.urls import include, path

urlpatterns = [
    path(
        "", include(("payments.providers.stripe.urls", "payments"), namespace="stripe")
    )
]
