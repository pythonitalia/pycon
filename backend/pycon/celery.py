from datetime import timedelta
import logging
import os
from celery import Celery
from celery.signals import worker_process_init
from opentelemetry.instrumentation.celery import CeleryInstrumentor

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
        from files_upload.tasks import delete_unused_files
        from pycon.tasks import check_for_idle_heavy_processing_workers

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
    except Exception:
        logger.exception("setup_periodic_tasks")


@worker_process_init.connect(weak=False)
def init_celery_tracing(*args, **kwargs):
    CeleryInstrumentor().instrument()
