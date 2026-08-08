from io import BufferedReader, BytesIO
import shutil
import subprocess
import zipfile
from django.core.files.storage import storages
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum
import os
import tempfile
import threading
import requests
from urllib.parse import parse_qs, unquote, urlparse
from google_api.exceptions import NoGoogleCloudQuotaLeftError
from google_api.sdk import (
    DRIVE_API_URL,
    drive_file_metadata,
    drive_headers,
    drive_list_files_in_folder,
    get_drive_credentials,
)
from pycon.storages import CustomS3Boto3Storage
from pycon.constants import GB, MB
from video_uploads.models import VideosImportRequest
import boto3
import botocore
from boto3.s3.transfer import TransferConfig

logger = logging.getLogger(__name__)


def is_s3_storage(storage):
    return type(storage) is CustomS3Boto3Storage


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


class UnsupportedVideoImportUrlError(Exception):
    pass


class DriveResourceKind(Enum):
    FILE = "file"
    FOLDER = "folder"


@dataclass
class DriveResource:
    kind: DriveResourceKind
    id: str


def parse_drive_url(source_url: str) -> DriveResource:
    parsed_url = urlparse(source_url)

    if parsed_url.hostname != "drive.google.com":
        raise UnsupportedVideoImportUrlError(
            f"Unsupported Google Drive URL: {source_url}"
        )

    path_segments = [segment for segment in parsed_url.path.split("/") if segment]

    # /file/d/<id>/view, /file/d/<id>/edit, /file/d/<id>
    if path_segments[:2] == ["file", "d"] and len(path_segments) > 2:
        return DriveResource(kind=DriveResourceKind.FILE, id=path_segments[2])

    # /drive/folders/<id>, /drive/u/0/folders/<id>
    if "folders" in path_segments:
        folders_at = path_segments.index("folders")
        if folders_at + 1 < len(path_segments):
            return DriveResource(
                kind=DriveResourceKind.FOLDER, id=path_segments[folders_at + 1]
            )

    # /open?id=<id>
    if path_segments[:1] == ["open"]:
        file_id = parse_qs(parsed_url.query).get("id", [""])[0]
        if file_id:
            return DriveResource(kind=DriveResourceKind.FILE, id=file_id)

    raise UnsupportedVideoImportUrlError(
        f"Unsupported Google Drive URL: {source_url}. Use a file link "
        f"(/file/d/<id>/view) or a folder link (/drive/folders/<id>)."
    )


class BaseTransferProcessing:
    """Shared machinery to import one or more blobs into the conference storage.

    Subclasses resolve the source link and enumerate the files to import, then
    hand each one to import_blob by setting download_link, filename, extension
    and transfer_total_size.
    """

    def __init__(self, videos_import_request: VideosImportRequest) -> None:
        self.videos_import_request = videos_import_request
        self.merged_file = None

    def run(self) -> list[str]:
        raise NotImplementedError

    def setup(self):
        self.storage = storages["default"]
        self.s3_client = self._get_s3_client()

    def executor(self) -> ThreadPoolExecutor:
        return ThreadPoolExecutor(max_workers=os.cpu_count() * 2)

    def download_headers(self) -> dict:
        """Headers sent with every ranged download request, merged with Range."""
        return {}

    @property
    def blob_directory(self) -> str:
        """Folder holding the blob being imported, empty at the import root."""
        directory = os.path.dirname(self.filename)
        return f"{directory}/" if directory else ""

    def import_blob(self, executor: ThreadPoolExecutor) -> list[str]:
        logger.info(
            "Importing blob for videos_import_request %s", self.videos_import_request.id
        )
        parts_info = self.determine_parts_info(self.transfer_total_size)

        logger.info(
            "Total size to download %s bytes, file parts %s for videos_import_request %s",
            self.transfer_total_size,
            parts_info,
            self.videos_import_request.id,
        )

        self.has_multiple_parts = len(parts_info) > 1

        parts = self.download_file(parts_info, executor)
        self.merge_parts(parts)
        try:
            with open(self.merged_file.name, "rb") as full_file:
                return self.process_downloaded_file(full_file, executor)
        finally:
            self.cleanup()

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
        # A zip is a container: its entries belong where the zip itself sits,
        # so a zip imported from a subfolder keeps that subfolder. Without
        # this, two subfolders shipping the same entry name overwrite one
        # another. A zip at the root has no prefix, as before.
        remote_filename = f"{self.blob_directory}{filename}"

        with zip_ref.open(filename) as file_obj:
            self.save_file_to_s3(remote_filename, file_obj)

        return remote_filename

    def save_file_to_s3(self, filename: str, file_data: BytesIO):
        logger.info(
            "Uploading file %s to S3 for videos_import_request %s",
            filename,
            self.videos_import_request.id,
        )

        conference = self.videos_import_request.conference
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
            self.merged_file = None

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
            "Finished downloading all parts for videos_import_request %s",
            self.videos_import_request.id,
        )
        return parts_paths

    def merge_parts(self, parts: list[str]):
        if not self.has_multiple_parts:
            self.merged_file = open(parts[0], "rb")
            return

        logger.info(
            "Merging parts for videos_import_request %s",
            self.videos_import_request.id,
        )

        self.merged_file = tempfile.NamedTemporaryFile(
            "wb",
            prefix=f"videos_import_{self.videos_import_request.id}",
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
                    f"Failed to download part {str(part_info)} for videos_import_request {self.videos_import_request.id}"
                )

            part_file = tempfile.NamedTemporaryFile(
                "wb",
                prefix=f"videos_import_{self.videos_import_request.id}.part{part_info.part_number}",
                suffix=self.extension,
                delete=False,
            )

            logger.info(
                "Downloading part %s for videos_import_request %s. Destination = %s. Attempt = %s",
                str(part_info),
                self.videos_import_request.id,
                part_file.name,
                attempts,
            )

            headers = {**self.download_headers(), **part_info.http_range_header}

            with requests.get(
                self.download_link, headers=headers, stream=True
            ) as response:
                response.raise_for_status()
                shutil.copyfileobj(response.raw, part_file, length=512 * MB)

            part_file.flush()
            os.fsync(part_file.fileno())
            part_disk_size = os.path.getsize(part_file.name)

            if part_disk_size != part_info.size:
                logger.warning(
                    "Downloaded part %s size does not match the expected size %s (file size %s) for videos_import_request %s. Trying again",
                    str(part_info),
                    part_info.size,
                    part_disk_size,
                    self.videos_import_request.id,
                )
                attempts += 1
                os.remove(part_file.name)
                continue

            logger.info(
                "Downloaded part %s for videos_import_request %s",
                str(part_info),
                self.videos_import_request.id,
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

    def _get_s3_client(self):
        if not is_s3_storage(self.storage):
            return None

        client_config = botocore.config.Config(
            max_pool_connections=100,
        )
        return boto3.client("s3", config=client_config)


class WetransferProcessing(BaseTransferProcessing):
    def run(self) -> list[str]:
        self.setup()
        self.download_link = self.get_download_link()
        self.filename, self.extension = self.get_filename_and_extension()
        self.transfer_total_size = self.get_file_total_size()

        with self.executor() as executor:
            return self.import_blob(executor)

    def get_download_link(self) -> str:
        wetransfer_url = self.videos_import_request.source_url
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


GOOGLE_APPS_MIME_PREFIX = "application/vnd.google-apps."
DRIVE_FOLDER_MIME_TYPE = f"{GOOGLE_APPS_MIME_PREFIX}folder"


def is_google_native(metadata: dict) -> bool:
    """Docs, Sheets, Slides and shortcuts have no bytes to download.

    Folders are google-apps types too, so callers must rule them out first.
    """
    return metadata.get("mimeType", "").startswith(GOOGLE_APPS_MIME_PREFIX)


class GoogleDriveProcessing(BaseTransferProcessing):
    def __init__(self, videos_import_request: VideosImportRequest) -> None:
        super().__init__(videos_import_request)
        self.credentials = None
        self.credentials_lock = threading.Lock()

    def run(self) -> list[str]:
        logger.info(
            "Running Google Drive processing for videos_import_request %s",
            self.videos_import_request.id,
        )
        self.setup()

        try:
            # Resolved once and passed to every later Drive call: a folder
            # shared with one Google account is invisible to another, so an
            # import that switched account midway would fail with a puzzling
            # 403 on files the organizer can see.
            self.credentials = get_drive_credentials()
        except NoGoogleCloudQuotaLeftError as e:
            # The exception carries no message, and an empty failed_reason
            # leaves the organizer with nothing to act on.
            raise Exception(
                "No Google account with Drive access is available. Authorize a "
                "Google account with the Drive scope from the admin, under "
                "Google Cloud OAuth Credentials, then retry the import."
            ) from e

        resource = parse_drive_url(self.videos_import_request.source_url)

        try:
            with self.executor() as executor:
                match resource.kind:
                    case DriveResourceKind.FOLDER:
                        return self.import_folder(resource.id, executor)
                    case DriveResourceKind.FILE:
                        return self.import_file_by_id(resource.id, executor)
        except requests.HTTPError as e:
            raise self.readable_drive_error(e) from e

    def readable_drive_error(self, error: requests.HTTPError) -> Exception:
        status_code = error.response.status_code if error.response is not None else None

        match status_code:
            case 401 | 403:
                return Exception(
                    f"Google denied access to this Drive item (HTTP {status_code}). "
                    f"The connected Google account may predate the Drive scope: "
                    f"re-authorize it from the admin, and check the file or folder "
                    f"is shared with it."
                )
            case 404:
                return Exception(
                    "This Drive file or folder was not found. Check the link, and "
                    "that it is shared with the connected Google account."
                )

        return error

    def download_headers(self) -> dict:
        # Parts download in parallel and a token can expire mid-transfer, so
        # every attempt asks for headers again under a lock.
        with self.credentials_lock:
            return drive_headers(self.credentials)

    def import_file_by_id(
        self, file_id: str, executor: ThreadPoolExecutor
    ) -> list[str]:
        logger.info(
            "Importing file by id %s for videos_import_request %s",
            file_id,
            self.videos_import_request.id,
        )
        metadata = drive_file_metadata(file_id=file_id, credentials=self.credentials)

        if is_google_native(metadata):
            raise Exception(
                f"{metadata['name']} is a Google-native file "
                f"({metadata['mimeType']}) and cannot be downloaded. Export it to "
                f"a regular file and share that instead."
            )

        return self.import_file(metadata, metadata["name"], executor)

    def import_folder(self, folder_id: str, executor: ThreadPoolExecutor) -> list[str]:
        logger.info(
            "Importing folder %s for videos_import_request %s",
            folder_id,
            self.videos_import_request.id,
        )
        imported_files = []

        for metadata, relative_path in self.walk_folder(folder_id, ""):
            imported_files.extend(self.import_file(metadata, relative_path, executor))

        return imported_files

    def walk_folder(self, folder_id: str, prefix: str):
        logger.info(
            "Walking folder %s for videos_import_request %s",
            folder_id,
            self.videos_import_request.id,
        )
        """Yield (metadata, path relative to the shared folder) for every file."""
        for item in drive_list_files_in_folder(
            folder_id=folder_id, credentials=self.credentials
        ):
            path = f"{prefix}{item['name']}"

            if item["mimeType"] == DRIVE_FOLDER_MIME_TYPE:
                yield from self.walk_folder(item["id"], f"{path}/")
                continue

            if is_google_native(item):
                logger.info(
                    "Skipping %s (%s), it has no downloadable content, "
                    "for videos_import_request %s",
                    path,
                    item["mimeType"],
                    self.videos_import_request.id,
                )
                continue

            logger.info(
                "Yielding item %s for videos_import_request %s",
                item,
                self.videos_import_request.id,
            )
            yield item, path

    def import_file(
        self, metadata: dict, filename: str, executor: ThreadPoolExecutor
    ) -> list[str]:
        logger.info(
            "Importing file %s for videos_import_request %s",
            filename,
            self.videos_import_request.id,
        )
        self.filename = filename
        _, self.extension = os.path.splitext(metadata["name"])
        self.transfer_total_size = int(metadata["size"])
        self.download_link = (
            f"{DRIVE_API_URL}/files/{metadata['id']}?alt=media&supportsAllDrives=true"
        )

        return self.import_blob(executor)


PROCESSING_CLASSES_BY_HOSTNAME = {
    "wetransfer.com": WetransferProcessing,
    "www.wetransfer.com": WetransferProcessing,
    "drive.google.com": GoogleDriveProcessing,
}


def get_processing_class(source_url: str) -> type[BaseTransferProcessing]:
    hostname = urlparse(source_url).hostname or ""

    try:
        return PROCESSING_CLASSES_BY_HOSTNAME[hostname]
    except KeyError:
        raise UnsupportedVideoImportUrlError(
            f"Unsupported import URL: {hostname or source_url} is not a supported provider."
        ) from None


def is_file_allowed(file_info: zipfile.ZipInfo) -> bool:
    filename = file_info.filename

    if file_info.is_dir():
        return False

    if "__MACOSX" in filename:
        return False

    if ".DS_Store" in filename:
        return False

    return True
