import logfire
from functools import wraps

from django.utils import timezone
from django.core.files.storage import storages
from io import BytesIO
import zipfile
import os
import tempfile
from urllib.parse import urlparse, unquote

import requests
from video_uploads.models import WetransferToS3TransferRequest
from pycon.celery import app


def wetransfer_error_handling(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logfire.exception(
                "Error processing wetransfer to s3 transfer request: {exc}", exc=e
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
        logfire.warn(
            "WetransferToS3TransferRequest with id={request_id} is not in QUEUED status, skipping",
            request_id=request_id,
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

    if response.status_code == 403:
        raise Exception("Wetransfer download link expired")

    response.raise_for_status()

    wetransfer_response = response.json()
    direct_link = wetransfer_response["direct_link"]
    parsed_direct_url = urlparse(direct_link)
    direct_link_filename = unquote(parsed_direct_url.path.split("/")[-1])
    _, ext = os.path.splitext(direct_link_filename)

    imported_files = []
    storage = storages["default"]

    temp_file = tempfile.NamedTemporaryFile(
        "wb", prefix=f"wetransfer_{wetransfer_to_s3_transfer_request.id}", suffix=ext
    )

    def save_file(filename, obj):
        imported_files.append(filename)
        storage.save(
            f"conference-videos/{conference.code}/{filename}",
            obj,
        )

    try:
        with requests.get(direct_link, stream=True) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=65536):
                if chunk:  # pragma: no cover
                    temp_file.write(chunk)

            temp_file.flush()

        with open(temp_file.name, "rb") as temp_file_read:
            match ext[1:]:
                case "zip":
                    # read the zip upload all files to s3
                    with zipfile.ZipFile(temp_file_read, "r") as zip_ref:
                        for file_info in zip_ref.infolist():
                            if not is_file_allowed(file_info):
                                continue

                            filename = file_info.filename
                            with zip_ref.open(filename) as file_obj:
                                file_data = BytesIO(file_obj.read())
                                save_file(filename, file_data)
                case _:
                    save_file(direct_link_filename, temp_file_read)
    finally:
        temp_file.close()

    wetransfer_to_s3_transfer_request.status = WetransferToS3TransferRequest.Status.DONE
    wetransfer_to_s3_transfer_request.imported_files = imported_files
    wetransfer_to_s3_transfer_request.finished_at = timezone.now()
    wetransfer_to_s3_transfer_request.save(
        update_fields=["status", "imported_files", "finished_at"]
    )


def is_file_allowed(file_info):
    filename = file_info.filename

    if file_info.is_dir():
        return False

    if "__MACOSX" in filename:
        return False

    if ".DS_Store" in filename:
        return False

    return True
