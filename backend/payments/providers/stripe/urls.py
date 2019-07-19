from django.urls import path

from .views import order_webhook

urlpatterns = [path("stripe/process-order/", order_webhook, name="process-order")]
