import time
from django.db import transaction
from django.conf import settings
import requests
import tempfile
from pycon.celery_utils import TaskWithLock
import pyclamd

from datetime import timedelta
import logging

from files_upload.models import File
from pycon.celery import app
from django.utils import timezone
from magika import Magika
from pathlib import Path

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


@app.task(base=TaskWithLock)
@transaction.atomic
def post_process_file_upload(file_id: str):
    breakpoint()
    logger.info("Processing file_id=%s", file_id)
    magika = Magika()

    with tempfile.NamedTemporaryFile() as temp_file:
        file = File.objects.select_for_update().get(id=file_id)
        if file.file.storage.is_remote:
            with requests.get(file.url, stream=True) as response:
                response.raise_for_status()

                for chunk in response.iter_content():
                    temp_file.write(chunk)

            file_path = temp_file.name
            file_handle = temp_file
        else:
            file_path = file.file.path
            file_handle = file.file.open("rb")

        magika_result = magika.identify_path(Path(file_path))
        file.mime_type = magika_result.output.mime_type

        attempts = 0
        while attempts < 3:
            try:
                virus_scanner = pyclamd.ClamdNetworkSocket(
                    host=settings.CLAMAV_HOST, port=settings.CLAMAV_PORT, timeout=10
                )
                result = virus_scanner.scan_stream(file_handle)
                virus_found = bool(result and result[file_path][0] == "FOUND")
                file.virus = virus_found
                break
            except pyclamd.ConnectionError:
                logger.exception(
                    "Could not connect to clamd server (attempt: %s)", attempts
                )
                attempts = attempts + 1
                time.sleep(attempts)

        file.save(update_fields=["virus", "mime_type"])
