from django.conf import settings
import requests
import tempfile
import pyclamd

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


@app.task
def post_process_file_upload(file_id: str):
    file = File.objects.get(id=file_id)

    with tempfile.NamedTemporaryFile() as temp_file:
        with requests.get(file.url, stream=True) as response:
            response.raise_for_status()

            for chunk in response.iter_content():
                temp_file.write(chunk)

            file_path = temp_file.name

        try:
            virus_scanner = pyclamd.ClamdNetworkSocket(
                host=settings.CLAMAV_HOST, port=settings.CLAMAV_PORT, timeout=10
            )
            result = virus_scanner.scan_stream(temp_file)
            virus_found = bool(result and result[file_path][0] == "FOUND")
            file.virus = virus_found
            file.save(update_fields=["virus"])
        except pyclamd.ConnectionError:
            logger.exception("Could not connect to clamd server")
