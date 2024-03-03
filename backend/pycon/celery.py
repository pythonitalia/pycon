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
    import django

    django.setup()

    try:
        from association_membership.tasks import (
            check_association_membership_subscriptions,
        )
        from schedule.tasks import process_schedule_items_videos_to_upload

        add = sender.add_periodic_task

        add(timedelta(minutes=5), check_association_membership_subscriptions)
        add(timedelta(minutes=10), process_schedule_items_videos_to_upload)
    except Exception:
        logger.exception("setup_periodic_tasks")
