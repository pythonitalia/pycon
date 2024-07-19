from concurrent.futures import ThreadPoolExecutor
import logging
from functools import wraps

from django.utils import timezone
from django.core.files.storage import storages
from io import BytesIO
import zipfile
import os
import tempfile
from urllib.parse import urlparse, unquote

import requests
from pycon.constants import KB
from video_uploads.models import WetransferToS3TransferRequest
from pycon.celery import app


logger = logging.getLogger(__name__)


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
        logger.warn(
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

    def save_file(filename, obj):
        imported_files.append(filename)
        storage.save(
            f"conference-videos/{conference.code}/{filename}",
            obj,
        )

    def download_chunk(start, end, index):
        logger.info(
            "Downloading chunk %s-%s for wetransfer_to_s3_transfer_request %s",
            start,
            end,
            wetransfer_to_s3_transfer_request.id,
        )
        part_file = tempfile.NamedTemporaryFile(
            "wb",
            prefix=f"wetransfer_{wetransfer_to_s3_transfer_request.id}.part{index}",
            suffix=ext,
        )

        headers = {"Range": f"bytes={start}-{end}"}
        with requests.get(direct_link, headers=headers, stream=True) as response:
            for chunk in response.iter_content(chunk_size=512 * KB):
                if chunk:  # pragma: no cover
                    part_file.write(chunk)

        part_file.flush()
        return open(part_file.name, "rb")

    num_chunks = 4
    try:
        head_response = requests.head(direct_link)
        file_size = int(head_response.headers["Content-Length"])
        chunk_size = file_size // num_chunks
        files_parts = []

        with ThreadPoolExecutor(max_workers=num_chunks) as executor:
            futures = []
            for i in range(num_chunks):
                start = i * chunk_size
                end = start + chunk_size - 1 if i < num_chunks - 1 else file_size
                futures.append(executor.submit(download_chunk, start, end, i))

            for future in futures:
                files_parts.append(future.result())

            full_file = tempfile.NamedTemporaryFile(
                "wb",
                prefix=f"wetransfer_{wetransfer_to_s3_transfer_request.id}",
                suffix=ext,
            )

            for part_id, file_part in enumerate(files_parts):
                logger.info(
                    "Merging file parts of transfer %s (part id %s)",
                    wetransfer_to_s3_transfer_request.id,
                    part_id,
                )

                full_file.write(file_part.read())
                file_part.close()

            full_file.flush()

        with open(full_file.name, "rb") as temp_file_read:
            match ext[1:]:
                case "zip":
                    logger.info(
                        "Unzipping file for wetransfer_to_s3_transfer_request %s",
                        wetransfer_to_s3_transfer_request.id,
                    )
                    # read the zip upload all files to s3
                    with zipfile.ZipFile(temp_file_read, "r") as zip_ref:
                        for file_info in zip_ref.infolist():
                            if not is_file_allowed(file_info):
                                continue

                            filename = file_info.filename
                            logger.info(
                                "Processing file %s of transfer request %s",
                                filename,
                                wetransfer_to_s3_transfer_request.id,
                            )

                            with zip_ref.open(filename) as file_obj:
                                file_data = BytesIO(file_obj.read())
                                save_file(filename, file_data)
                case _:
                    logger.info(
                        "Uploading file for wetransfer_to_s3_transfer_request %s",
                        wetransfer_to_s3_transfer_request.id,
                    )
                    save_file(direct_link_filename, temp_file_read)
    finally:
        full_file.close()

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
