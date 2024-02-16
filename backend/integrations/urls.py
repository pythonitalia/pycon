from django.urls import path
from integrations.views import plain_customer_cards


urlpatterns = [
    path("plain/customer-cards", plain_customer_cards),
]
