from io import BufferedReader, BytesIO
import zipfile
from django.core.files.storage import storages
import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import os
import tempfile
import requests
from urllib.parse import unquote, urlparse
from pycon.constants import GB, KB, MB
from video_uploads.models import WetransferToS3TransferRequest


logger = logging.getLogger(__name__)


@dataclass
class DownloadPart:
    index: int
    start: int
    end: int

    @property
    def header(self):
        return {"Range": f"bytes={self.start}-{self.end}"}


class WetransferProcessing:
    def __init__(
        self, wetransfer_to_s3_transfer_request: WetransferToS3TransferRequest
    ) -> None:
        self.wetransfer_to_s3_transfer_request = wetransfer_to_s3_transfer_request
        self.imported_files = []
        self.full_file_name = None
        self.parts_refs = []

    def run(self) -> list[str]:
        self.storage = storages["default"]
        self.download_link = self.get_download_link()
        self.filename, self.extension = self.get_filename_and_extension()

        file_total_size = self.get_file_total_size()
        download_parts = self.determine_download_parts(file_total_size)
        self.has_multiple_parts = len(download_parts) > 1

        logger.info(
            "Total size to download %s bytes, file parts %s for wetransfer_to_s3_transfer_request %s",
            file_total_size,
            download_parts,
            self.wetransfer_to_s3_transfer_request.id,
        )

        max_workers = os.cpu_count() * 2

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            self.parts_refs = self.download_parts(download_parts, executor)
            try:
                self.full_file_name = self.merge_parts(self.parts_refs)

                with open(self.full_file_name, "rb") as full_file:
                    imported_files = self.process_downloaded_file(full_file, executor)
            finally:
                self.cleanup()

        return imported_files

    def process_downloaded_file(
        self, full_file: BufferedReader, executor: ThreadPoolExecutor
    ):
        extension = self.extension[1:]
        match extension:
            case "zip":
                imported_files = self.process_zip_file(full_file, executor)
            case _:
                imported_files = [self.save_file_to_s3(self.filename, full_file)]

        return imported_files

    def process_zip_file(
        self, full_file: BufferedReader, executor: ThreadPoolExecutor
    ) -> list[str]:
        futures = []
        with zipfile.ZipFile(full_file, "r") as zip_ref:
            for file_info in zip_ref.infolist():
                if not is_file_allowed(file_info):
                    continue

                filename = file_info.filename
                file_obj = zip_ref.open(filename)
                futures.append(
                    executor.submit(self.process_zip_file_obj, file_obj, filename)
                )

        return [future.result() for future in futures]

    def process_zip_file_obj(self, file_obj: BufferedReader, filename: str):
        logger.info(
            "Processing zip file %s for wetransfer_to_s3_transfer_request %s",
            filename,
            self.wetransfer_to_s3_transfer_request.id,
        )

        try:
            file_data = BytesIO()
            while True:
                chunk = file_obj.read(500 * MB)

                if not chunk:
                    break

                file_data.write(chunk)

            self.save_file_to_s3(filename, file_data)
            return filename
        finally:
            file_obj.close()

    def save_file_to_s3(self, filename: str, file_data: BytesIO):
        logger.info(
            "Uploading file %s to S3 for wetransfer_to_s3_transfer_request %s",
            filename,
            self.wetransfer_to_s3_transfer_request.id,
        )

        conference = self.wetransfer_to_s3_transfer_request.conference
        self.storage.save(
            f"conference-videos/{conference.code}/{filename}",
            file_data,
        )
        return filename

    def cleanup(self):
        if self.full_file_name:
            os.unlink(self.full_file_name)

        if self.has_multiple_parts:
            for part in self.parts_refs:
                self.storage.delete(part)

    def merge_parts(self, parts_refs: list[str]) -> str:
        if not self.has_multiple_parts:
            logger.info(
                "No multiple parts for wetransfer_to_s3_transfer_request %s",
                self.wetransfer_to_s3_transfer_request.id,
            )
            return parts_refs[0]

        logger.info(
            "Merging parts for wetransfer_to_s3_transfer_request %s",
            self.wetransfer_to_s3_transfer_request.id,
        )

        merged_file = tempfile.NamedTemporaryFile(
            "wb",
            prefix=f"wetransfer_{self.wetransfer_to_s3_transfer_request.id}",
            suffix=self.extension,
            delete=False,
        )

        for s3_path in parts_refs:
            logger.info(
                "Downloading part %s from S3 for wetransfer_to_s3_transfer_request %s",
                s3_path,
                self.wetransfer_to_s3_transfer_request.id,
            )

            file_part = self.storage.open(s3_path)
            while True:
                chunk = file_part.read(500 * MB)

                if not chunk:
                    break

                merged_file.write(chunk)
            merged_file.flush()

        return merged_file.name

    def download_parts(
        self, download_parts: list[DownloadPart], executor: ThreadPoolExecutor
    ) -> list[str]:
        parts_futures = []
        parts_paths = []

        for download_part in download_parts:
            parts_futures.append(executor.submit(self.download_part, download_part))

        for future in parts_futures:
            parts_paths.append(future.result())

        logger.info(
            "Finished downloading all parts for wetransfer_to_s3_transfer_request %s",
            self.wetransfer_to_s3_transfer_request.id,
        )
        return parts_paths

    def download_part(self, download_part: DownloadPart) -> str:
        logger.info(
            "Downloading chunk %s-%s for wetransfer_to_s3_transfer_request %s",
            download_part.start,
            download_part.end,
            self.wetransfer_to_s3_transfer_request.id,
        )

        part_file = tempfile.NamedTemporaryFile(
            "wb",
            prefix=f"wetransfer_{self.wetransfer_to_s3_transfer_request.id}.part{download_part.index}",
            suffix=self.extension,
            delete=False,
        )

        with requests.get(
            self.download_link, headers=download_part.header, stream=True
        ) as response:
            for chunk in response.iter_content(chunk_size=512 * KB):
                if chunk:  # pragma: no cover
                    part_file.write(chunk)

        part_file.flush()

        if not self.has_multiple_parts:
            return part_file.name

        logging.info(
            "Moving part file %s to S3 for wetransfer_to_s3_transfer_request %s",
            part_file.name,
            self.wetransfer_to_s3_transfer_request.id,
        )

        s3_path = self.file_part_s3_path(download_part)
        self.storage.save(
            s3_path,
            open(part_file.name, "rb"),
        )

        part_file.close()
        os.unlink(part_file.name)
        return s3_path

    def determine_download_parts(self, file_size: int) -> list[DownloadPart]:
        num_parts = self._determinate_total_num_of_parts(file_size)
        chunk_size = file_size // num_parts
        download_parts = []

        for i in range(num_parts):
            start = i * chunk_size
            end = start + chunk_size - 1 if i < num_parts - 1 else file_size
            download_parts.append(DownloadPart(index=i, start=start, end=end))

        return download_parts

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

    def file_part_s3_path(self, download_part: DownloadPart) -> str:
        return f"wetransfer-to-s3-transfers/{self.wetransfer_to_s3_transfer_request.id}/part{download_part.index}{self.extension}"


def is_file_allowed(file_info: zipfile.ZipInfo) -> bool:
    filename = file_info.filename

    if file_info.is_dir():
        return False

    if "__MACOSX" in filename:
        return False

    if ".DS_Store" in filename:
        return False

    return True
