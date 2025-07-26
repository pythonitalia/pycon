from io import BufferedReader, BytesIO
import shutil
import subprocess
import zipfile
from django.core.files.storage import storages
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import os
import tempfile
import requests
from urllib.parse import unquote, urlparse
from pycon.storages import CustomS3Boto3Storage
from pycon.constants import GB, MB
from video_uploads.models import WetransferToS3TransferRequest
import boto3
import botocore
from boto3.s3.transfer import TransferConfig

logger = logging.getLogger(__name__)


def is_s3_storage(storage):
    return type(storage) == CustomS3Boto3Storage


@dataclass
class PartInfo:
    part_number: int
    byte_start: int
    byte_end: int

    @property
    def http_range_header(self) -> dict:
        return {"Range": f"bytes={self.byte_start}-{self.last_byte}"}

    @property
    def last_byte(self) -> int:
        return self.byte_end - 1

    @property
    def size(self) -> int:
        return self.byte_end - self.byte_start

    def __str__(self):
        return f"Part {self.part_number} ({self.byte_start}-{self.last_byte})"


class WetransferProcessing:
    def __init__(
        self, wetransfer_to_s3_transfer_request: WetransferToS3TransferRequest
    ) -> None:
        self.wetransfer_to_s3_transfer_request = wetransfer_to_s3_transfer_request
        self.imported_files = []
        self.merged_file = None

    def run(self) -> list[str]:
        os.makedirs("/tmp/pycon/", exist_ok=True)

        self.storage = storages["default"]
        self.s3_client = self._get_s3_client()
        self.download_link = self.get_download_link()
        self.filename, self.extension = self.get_filename_and_extension()

        self.transfer_total_size = self.get_file_total_size()
        parts_info = self.determine_parts_info(self.transfer_total_size)

        logger.info(
            "Total size to download %s bytes, file parts %s for wetransfer_to_s3_transfer_request %s",
            self.transfer_total_size,
            parts_info,
            self.wetransfer_to_s3_transfer_request.id,
        )

        self.has_multiple_parts = len(parts_info) > 1

        max_workers = os.cpu_count() * 2

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            parts = self.download_file(parts_info, executor)
            self.merge_parts(parts)
            try:
                with open(self.merged_file.name, "rb") as full_file:
                    imported_files = self.process_downloaded_file(full_file, executor)
            finally:
                self.cleanup()

        return imported_files

    def process_downloaded_file(
        self, full_file: BufferedReader, executor: ThreadPoolExecutor
    ):
        match self.extension[1:]:
            case "zip":
                imported_files = self.process_zip_file(full_file, executor)
            case _:
                imported_files = [self.save_file_to_s3(self.filename, full_file)]

        return imported_files

    def process_zip_file(
        self, full_file: BufferedReader, executor: ThreadPoolExecutor
    ) -> list[str]:
        futures = []
        all_filenames = []

        zip_ref = zipfile.ZipFile(full_file, "r")
        try:
            for file_info in zip_ref.infolist():
                if not is_file_allowed(file_info):
                    continue

                filename = file_info.filename
                futures.append(
                    executor.submit(self.process_zip_file_obj, zip_ref, filename)
                )

            for future in as_completed(futures):
                all_filenames.append(future.result())
        finally:
            zip_ref.close()

        return all_filenames

    def process_zip_file_obj(self, zip_ref: zipfile.ZipFile, filename: str):
        with zip_ref.open(filename) as file_obj:
            self.save_file_to_s3(filename, file_obj)

        return filename

    def save_file_to_s3(self, filename: str, file_data: BytesIO):
        logger.info(
            "Uploading file %s to S3 for wetransfer_to_s3_transfer_request %s",
            filename,
            self.wetransfer_to_s3_transfer_request.id,
        )

        conference = self.wetransfer_to_s3_transfer_request.conference
        remote_path = f"conference-videos/{conference.code}/{filename}"
        if is_s3_storage(self.storage):
            config = TransferConfig(
                multipart_threshold=512 * MB,
                max_concurrency=8,
                multipart_chunksize=64 * MB,
                use_threads=True,
                max_io_queue=100,
            )

            self.s3_client.upload_fileobj(
                file_data, self.storage.bucket_name, remote_path, Config=config
            )
        else:
            self.storage.save(remote_path, file_data)
        return filename

    def cleanup(self):
        if self.merged_file:
            os.remove(self.merged_file.name)

    def download_file(
        self, parts_info: list[PartInfo], executor: ThreadPoolExecutor
    ) -> list[str]:
        futures = []
        parts_paths = []

        for part_info in parts_info:
            futures.append(executor.submit(self.download_part, part_info))

        for future in futures:
            filename = future.result()
            parts_paths.append(filename)

        logger.info(
            "Finished downloading all parts for wetransfer_to_s3_transfer_request %s",
            self.wetransfer_to_s3_transfer_request.id,
        )
        return parts_paths

    def merge_parts(self, parts: list[str]):
        if not self.has_multiple_parts:
            self.merged_file = open(parts[0], "rb")
            return

        logger.info(
            "Merging parts for wetransfer_to_s3_transfer_request %s",
            self.wetransfer_to_s3_transfer_request.id,
        )

        self.merged_file = tempfile.NamedTemporaryFile(
            "wb",
            prefix=f"/tmp/pycon/wetransfer_{self.wetransfer_to_s3_transfer_request.id}",
            suffix=self.extension,
            delete=False,
        )

        subprocess.run(["cat"] + parts, stdout=open(self.merged_file.name, "wb"))

        for part in parts:
            os.remove(part)

    def download_part(self, part_info: PartInfo) -> str:
        attempts = 1

        while True:
            if attempts > 3:
                raise Exception(
                    f"Failed to download part {str(part_info)} for wetransfer_to_s3_transfer_request {self.wetransfer_to_s3_transfer_request.id}"
                )

            part_file = tempfile.NamedTemporaryFile(
                "wb",
                prefix=f"/tmp/pycon/wetransfer_{self.wetransfer_to_s3_transfer_request.id}.part{part_info.part_number}",
                suffix=self.extension,
                delete=False,
            )

            logger.info(
                "Downloading part %s for wetransfer_to_s3_transfer_request %s. Destination = %s. Attempt = %s",
                str(part_info),
                self.wetransfer_to_s3_transfer_request.id,
                part_file.name,
                attempts,
            )

            with requests.get(
                self.download_link, headers=part_info.http_range_header, stream=True
            ) as response:
                response.raise_for_status()
                shutil.copyfileobj(response.raw, part_file, length=512 * MB)

            part_file.flush()
            os.fsync(part_file.fileno())
            part_disk_size = os.path.getsize(part_file.name)

            if part_disk_size != part_info.size:
                logger.warning(
                    "Downloaded part %s size does not match the expected size %s (file size %s) for wetransfer_to_s3_transfer_request %s. Trying again",
                    str(part_info),
                    part_info.size,
                    part_disk_size,
                    self.wetransfer_to_s3_transfer_request.id,
                )
                attempts += 1
                os.remove(part_file.name)
                continue

            logger.info(
                "Downloaded part %s for wetransfer_to_s3_transfer_request %s",
                str(part_info),
                self.wetransfer_to_s3_transfer_request.id,
            )
            return part_file.name

    def determine_parts_info(self, file_size: int) -> list[PartInfo]:
        num_parts = self._determinate_total_num_of_parts(file_size)
        chunk_size = file_size // num_parts
        parts_info = []

        for i in range(num_parts):
            byte_start = i * chunk_size
            byte_end = byte_start + chunk_size if i < num_parts - 1 else file_size
            parts_info.append(
                PartInfo(part_number=i + 1, byte_start=byte_start, byte_end=byte_end)
            )

        return parts_info

    def _determinate_total_num_of_parts(self, file_size: int) -> int:
        if file_size >= 50 * GB:
            return 8

        if file_size >= 10 * GB:
            return 4

        return 1

    def get_file_total_size(self) -> int:
        head_response = requests.head(self.download_link)
        return int(head_response.headers["Content-Length"])

    def get_download_link(self) -> str:
        wetransfer_url = self.wetransfer_to_s3_transfer_request.wetransfer_url
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
        return direct_link

    def get_filename_and_extension(self):
        parsed_url = urlparse(self.download_link)
        direct_link_filename = unquote(parsed_url.path.split("/")[-1])
        _, ext = os.path.splitext(direct_link_filename)
        return direct_link_filename, ext

    def _get_s3_client(self):
        if not is_s3_storage(self.storage):
            return None

        client_config = botocore.config.Config(
            max_pool_connections=100,
        )
        return boto3.client("s3", config=client_config)


def is_file_allowed(file_info: zipfile.ZipInfo) -> bool:
    filename = file_info.filename

    if file_info.is_dir():
        return False

    if "__MACOSX" in filename:
        return False

    if ".DS_Store" in filename:
        return False

    return True
