import inspect
import requests
from google_api.exceptions import NoGoogleCloudQuotaLeftError
from google_api.models import GoogleCloudOAuthCredential, UsedRequestQuota
from googleapiclient.discovery import build
from apiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


GOOGLE_CLOUD_SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/drive.readonly",
]

DRIVE_API_URL = "https://www.googleapis.com/drive/v3"
DRIVE_LIST_PAGE_SIZE = 1000


def get_available_credentials(service, min_quota):
    token = GoogleCloudOAuthCredential.get_available_credentials_token(
        service=service, min_quota=min_quota
    )

    if not token:
        raise NoGoogleCloudQuotaLeftError()

    return Credentials.from_authorized_user_info(
        {
            "token": token.token,
            "refresh_token": token.refresh_token,
            "token_uri": token.token_uri,
            "client_id": token.client_id,
            "client_secret": token.client_secret,
            "scopes": GOOGLE_CLOUD_SCOPES,
        }
    )


def count_quota(service: str, quota: int):
    def _add_quota(credentials):
        credential_object = GoogleCloudOAuthCredential.objects.get_by_client_id(
            credentials.client_id
        )

        UsedRequestQuota.objects.create(
            credentials=credential_object,
            cost=quota,
            service=service,
        )

    def wrapper(func):
        if inspect.isgeneratorfunction(func):

            def wrapped(*args, **kwargs):
                credentials = get_available_credentials(service, quota)
                try:
                    for value in func(*args, credentials=credentials, **kwargs):
                        yield value
                finally:
                    _add_quota(credentials)

        else:

            def wrapped(*args, **kwargs):
                credentials = get_available_credentials(service, quota)
                try:
                    ret_value = func(*args, credentials=credentials, **kwargs)
                finally:
                    _add_quota(credentials)
                return ret_value

        return wrapped

    return wrapper


def refreshed(credentials: Credentials) -> Credentials:
    """Credentials rebuilt from a stored token carry no expiry, so google-auth
    treats them as expired and credentials.token is the stale stored value.
    googleapiclient refreshes lazily on its own; direct requests calls must not.
    """
    if not credentials.valid:
        credentials.refresh(Request())

    return credentials


def drive_headers(credentials: Credentials) -> dict:
    return {"Authorization": f"Bearer {refreshed(credentials).token}"}


@count_quota("drive", 1)
def get_drive_credentials(*, credentials: Credentials) -> Credentials:
    """Refreshed credentials for callers that drive their own Drive requests."""
    return refreshed(credentials)


@count_quota("drive", 1)
def drive_file_metadata(*, file_id: str, credentials: Credentials) -> dict:
    response = requests.get(
        f"{DRIVE_API_URL}/files/{file_id}",
        params={
            "fields": "id,name,size,mimeType",
            "supportsAllDrives": "true",
        },
        headers=drive_headers(credentials),
    )
    response.raise_for_status()
    return response.json()


@count_quota("drive", 1)
def drive_list_files_in_folder(*, folder_id: str, credentials: Credentials):
    headers = drive_headers(credentials)
    params = {
        "q": f"'{folder_id}' in parents and trashed = false",
        "fields": "nextPageToken,files(id,name,mimeType,size)",
        "pageSize": DRIVE_LIST_PAGE_SIZE,
        "supportsAllDrives": "true",
        "includeItemsFromAllDrives": "true",
    }

    while True:
        response = requests.get(
            f"{DRIVE_API_URL}/files", params=params, headers=headers
        )
        response.raise_for_status()
        payload = response.json()

        yield from payload.get("files", [])

        page_token = payload.get("nextPageToken")
        if not page_token:
            return

        params["pageToken"] = page_token


@count_quota("youtube", 1600)
def youtube_videos_insert(
    *,
    title: str,
    description: str,
    tags: str,
    file_path: str,
    credentials: Credentials,
):
    youtube = build("youtube", "v3", credentials=credentials)

    upload_request = youtube.videos().insert(
        part="snippet,status",
        notifySubscribers=False,
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            },
        },
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True),
    )

    response = None

    while response is None:
        status, response = upload_request.next_chunk()
        yield status

    if "id" in response:
        yield response
    else:
        raise ValueError("The upload failed with an unexpected response: %s" % response)


@count_quota("youtube", 50)
def youtube_videos_set_thumbnail(
    *, video_id: str, thumbnail_path: str, credentials: Credentials
):
    youtube = build("youtube", "v3", credentials=credentials)
    youtube.thumbnails().set(
        videoId=video_id, media_body=MediaFileUpload(thumbnail_path)
    ).execute()
