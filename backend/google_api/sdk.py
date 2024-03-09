import inspect
from google_api.exceptions import NoGoogleCloudQuotaLeftError
from google_api.models import GoogleCloudOAuthCredential, UsedRequestQuota
from googleapiclient.discovery import build
from apiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials


GOOGLE_CLOUD_SCOPES = ["https://www.googleapis.com/auth/youtube"]


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
