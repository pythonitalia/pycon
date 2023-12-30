from datetime import timedelta
import logging
import os
from celery import Celery

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pycon.settings.prod")

app = Celery("pycon")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        add = sender.add_periodic_task

        add(timedelta(minutes=2), debug_cron)
    except Exception:
        logger.exception("setup_periodic_tasks")


@app.task
def debug_cron():
    print("debug cron")
