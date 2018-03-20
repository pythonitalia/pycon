from django.apps import apps

from donations.apps import DonationsConfig


def test_apps():
    DonationsConfig.name == 'donations'
    apps.get_app_config('donations').name == 'donations'
