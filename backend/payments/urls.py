from django.urls import path, include


urlpatterns = [
    path('', include('payments.providers.stripe.urls')),
]
