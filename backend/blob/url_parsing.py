from dataclasses import dataclass
from typing import List, Optional

from blob.config import AZURE_STORAGE_URL_PARSE, get_account_name
from blob.enum import BlobContainer


@dataclass(frozen=True)
class ParsedAzureStorageUrl:
    account: str
    container: BlobContainer
    paths: List[str]

    @property
    def path(self) -> str:
        return "/".join(self.paths)


def verify_azure_storage_url(
    *, url: str, allowed_containers: List[BlobContainer]
) -> bool:
    parsed_url = parse_azure_storage_url(url)

    if not parsed_url:
        return False

    url_account = parsed_url.account
    url_container = parsed_url.container

    if url_account != get_account_name():
        return False

    if url_container not in allowed_containers:
        return False

    return True


def parse_azure_storage_url(url: str) -> Optional[ParsedAzureStorageUrl]:
    match = AZURE_STORAGE_URL_PARSE.fullmatch(url)

    if not match:
        return None

    account = match.group("account")
    container = match.group("container")
    paths = match.group("path").split("/")

    return ParsedAzureStorageUrl(
        account=account,
        container=BlobContainer(container),
        paths=paths,
    )
