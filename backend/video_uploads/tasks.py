from functools import wraps

from django.utils import timezone
from django.core.files.storage import storages
from io import BytesIO
import zipfile
import os
import tempfile
from urllib.parse import urlparse, unquote

import requests
import logging
from pycon.tasks import launch_heavy_processing_worker
from video_uploads.models import WetransferToS3TransferRequest
from pycon.celery import app
from django.db import transaction

logger = logging.getLogger(__name__)


@app.task
@transaction.atomic
def queue_wetransfer_to_s3_transfer_request(request_id):
    wetransfer_to_s3_transfer_request = WetransferToS3TransferRequest.objects.get(
        id=request_id
    )

    if (
        wetransfer_to_s3_transfer_request.status
        != WetransferToS3TransferRequest.Status.PENDING
    ):
        logger.warning(
            "WetransferToS3TransferRequest with id=%s is not in PENDING status, skipping",
            request_id,
        )
        return

    wetransfer_to_s3_transfer_request.status = (
        WetransferToS3TransferRequest.Status.QUEUED
    )
    wetransfer_to_s3_transfer_request.failed_reason = ""
    wetransfer_to_s3_transfer_request.save(update_fields=["status", "failed_reason"])

    def _on_commit():
        process_wetransfer_to_s3_transfer_request.apply_async(
            args=[request_id], queue="heavy_processing"
        )
        launch_heavy_processing_worker.delay()

    transaction.on_commit(_on_commit)


def wetransfer_error_handling(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(
                "Error processing wetransfer to s3 transfer request: %s", e
            )
            request_id = args[0]
            wetransfer_to_s3_transfer_request = (
                WetransferToS3TransferRequest.objects.get(id=request_id)
            )
            wetransfer_to_s3_transfer_request.status = (
                WetransferToS3TransferRequest.Status.FAILED
            )
            wetransfer_to_s3_transfer_request.failed_reason = str(e)
            wetransfer_to_s3_transfer_request.save(
                update_fields=["status", "failed_reason"]
            )

    return wrapper


@app.task
@wetransfer_error_handling
def process_wetransfer_to_s3_transfer_request(request_id):
    wetransfer_to_s3_transfer_request = WetransferToS3TransferRequest.objects.get(
        id=request_id
    )

    if (
        wetransfer_to_s3_transfer_request.status
        != WetransferToS3TransferRequest.Status.QUEUED
    ):
        logger.warning(
            "WetransferToS3TransferRequest with id=%s is not in QUEUED status, skipping",
            request_id,
        )
        return

    wetransfer_to_s3_transfer_request.status = (
        WetransferToS3TransferRequest.Status.PROCESSING
    )
    wetransfer_to_s3_transfer_request.started_at = timezone.now()
    wetransfer_to_s3_transfer_request.save(update_fields=["status", "started_at"])

    conference = wetransfer_to_s3_transfer_request.conference
    wetransfer_url = wetransfer_to_s3_transfer_request.wetransfer_url
    parsed_wetransfer_url = urlparse(wetransfer_url)

    hostname = parsed_wetransfer_url.hostname
    _, _, transfer_id, security_hash = parsed_wetransfer_url.path.split("/")

    response = requests.post(
        f"https://{hostname}/api/v4/transfers/{transfer_id}/download",
        json={"security_hash": security_hash, "intent": "entire_transfer"},
    )

    direct_link = response.json()["direct_link"]
    parsed_direct_url = urlparse(direct_link)
    direct_link_filename = unquote(parsed_direct_url.path.split("/")[-1])
    _, ext = os.path.splitext(direct_link_filename)

    imported_files = []
    storage = storages["default"]

    temp_file = tempfile.NamedTemporaryFile(
        "wb", prefix=f"wetransfer_{wetransfer_to_s3_transfer_request.id}", suffix=ext
    )

    try:
        with requests.get(direct_link, stream=True) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=None):
                if chunk:
                    temp_file.write(chunk)

        with open(temp_file.name, "rb") as temp_file_read:
            match ext[1:]:
                case "zip":
                    # read the zip upload all files to s3
                    with zipfile.ZipFile(temp_file_read, "r") as zip_ref:
                        for file_info in zip_ref.infolist():
                            filename = file_info.filename

                            if file_info.is_dir():
                                continue

                            if "__MACOSX" in filename:
                                continue

                            if ".DS_Store" in filename:
                                continue

                            with zip_ref.open(filename) as file_obj:
                                file_data = BytesIO(file_obj.read())
                                storage.save(
                                    f"conference-videos/{conference.code}/{filename}",
                                    file_data,
                                )
                                imported_files.append(filename)
                case _:
                    imported_files.append(direct_link_filename)
                    storage.save(
                        f"conference-videos/{conference.code}/{direct_link_filename}",
                        temp_file_read,
                    )
    finally:
        temp_file.close()

    wetransfer_to_s3_transfer_request.status = WetransferToS3TransferRequest.Status.DONE
    wetransfer_to_s3_transfer_request.imported_files = imported_files
    wetransfer_to_s3_transfer_request.finished_at = timezone.now()
    wetransfer_to_s3_transfer_request.save(
        update_fields=["status", "imported_files", "finished_at"]
    )
