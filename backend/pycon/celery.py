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

    from association_membership.tasks import (
        check_association_membership_subscriptions,
    )
    from schedule.tasks import process_schedule_items_videos_to_upload
    from files_upload.tasks import delete_unused_files
    from pycon.tasks import check_for_idle_heavy_processing_workers
    from notifications.tasks import send_pending_emails

    add = sender.add_periodic_task

    add(
        timedelta(minutes=5),
        check_association_membership_subscriptions,
        name="Check Python Italia memberships",
    )
    add(
        timedelta(minutes=30),
        process_schedule_items_videos_to_upload,
        name="Process schedule items videos to upload",
    )
    add(
        timedelta(minutes=60),
        delete_unused_files,
        name="Delete unused files",
    )
    add(
        timedelta(minutes=2),
        check_for_idle_heavy_processing_workers,
        name="Check for idle heavy processing workers",
    )
    add(
        timedelta(minutes=1),
        send_pending_emails,
        name="Send pending emails",
    )
