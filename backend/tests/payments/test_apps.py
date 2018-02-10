from django.apps import apps

from payments.apps import PaymentsConfig


def test_apps():
    PaymentsConfig.name == 'payments'
    apps.get_app_config('payments').name == 'payments'
