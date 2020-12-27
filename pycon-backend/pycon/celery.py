import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pycon.settings.celery")

app = Celery("pycon")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(["integrations"])
