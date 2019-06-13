from django.urls import path, include

from .views import order_webhook


urlpatterns = [
    path('stripe/process-order/', order_webhook)
]
