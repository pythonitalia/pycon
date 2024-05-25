import re

from django.conf import settings

AZURE_STORAGE_URL_PARSE = re.compile(
    r"https:\/\/(?P<account>.*)\.blob\.core\.windows\.net\/(?P<container>participants\-avatars|temporary\-uploads)/(?P<path>.*)"
)


def get_account_url() -> str:
    return f"https://{get_account_name()}.blob.core.windows.net/"


def get_account_name() -> str:
    return settings.AZURE_STORAGE_ACCOUNT_NAME


def get_account_key() -> str:
    return settings.AZURE_STORAGE_ACCOUNT_KEY


def _build_url(container: str, blob: str, sas_token: str = "") -> str:
    base = get_account_url()
    path = f"{container}/{blob}"
    return f"{base}{path}?{sas_token}" if sas_token else f"{base}{path}"
