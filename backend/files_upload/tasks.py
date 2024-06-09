from datetime import timedelta
import logging

from files_upload.models import File
from pycon.celery import app
from django.utils import timezone

logger = logging.getLogger(__name__)


@app.task
def delete_unused_files():
    logger.info("Deleting unused files")
    unused_files = File.objects.filter(participants__isnull=True).filter(
        created__lt=timezone.now() - timedelta(hours=24)
    )

    for unused_file in unused_files:
        logger.info("Deleting file_id=%s", unused_file.id)
        unused_file.file.delete(save=False)
        unused_file.delete()
