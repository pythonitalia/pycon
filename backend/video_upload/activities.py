import cv2
import logging
from dataclasses import dataclass
from typing import Any
from google_api.sdk import youtube_videos_insert, youtube_videos_set_thumbnail
from users.client import get_users_data_by_ids_async
from temporalio import activity
from schedule.models import ScheduleItem
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import storages

logger = logging.getLogger(__name__)

local_storage = FileSystemStorage()
local_storage.base_location = "/tmp/"


@dataclass
class ScheduleItemData:
    id: int
    slug: str
    title: str
    type: str
    description: str
    abstract: str
    elevator_pitch: str
    video_uploaded_path: str
    tags: list[str]
    speakers_ids: list[int]
    conference_name: str
    conference_youtube_video_bottom_text: str
    has_submission: bool

    @property
    def clean_tags(self) -> list[str]:
        return [tag.replace(" ", "").replace("-", "").lower() for tag in self.tags]

    @property
    def hashtags(self) -> list[str]:
        return [f"#{tag}" for tag in self.clean_tags]


@activity.defn
async def fetch_schedule_item(schedule_item_id: int) -> ScheduleItemData:
    schedule_item = await ScheduleItem.objects.prefetch_related(
        "submission",
        "submission__tags",
        "conference",
        "language",
        "additional_speakers",
        "keynote__speakers",
    ).aget(id=schedule_item_id)

    speakers_ids = schedule_item.speakers
    language_code = schedule_item.language.code

    return ScheduleItemData(
        id=schedule_item.id,
        slug=schedule_item.slug,
        type=schedule_item.type,
        title=schedule_item.title.strip(),
        description=schedule_item.description.strip(),
        abstract=schedule_item.submission.abstract.localize(language_code).strip()
        if schedule_item.submission_id
        else "",
        elevator_pitch=schedule_item.submission.elevator_pitch.localize(
            language_code
        ).strip()
        if schedule_item.submission_id
        else "",
        tags=[tag.name for tag in schedule_item.submission.tags.all()]
        if schedule_item.submission_id
        else [],
        video_uploaded_path=schedule_item.video_uploaded_path,
        speakers_ids=speakers_ids,
        conference_name=schedule_item.conference.name.localize(language_code),
        conference_youtube_video_bottom_text=schedule_item.conference.youtube_video_bottom_text,
        has_submission=schedule_item.submission_id is not None,
    )


@activity.defn
async def fetch_speakers_data(
    speakers_ids: list[int],
) -> dict[str, dict[str, Any]]:
    return await get_users_data_by_ids_async(speakers_ids)


@dataclass
class AddYouTubeIDToScheduleItemInput:
    schedule_item_id: int
    youtube_id: str


@activity.defn
async def add_youtube_id_to_schedule_item(
    input: AddYouTubeIDToScheduleItemInput,
) -> None:
    schedule_item = await ScheduleItem.objects.aget(id=input.schedule_item_id)
    schedule_item.youtube_video_id = input.youtube_id
    await schedule_item.asave(update_fields=["youtube_video_id"])


@dataclass
class DownloadVideoFileInput:
    path: str
    id: int


@activity.defn
async def download_video_file(input: DownloadVideoFileInput) -> str:
    logger.warning(f"downloading {input.path}")
    storage = storages["conferencevideos"]
    filename = f"yt_upload_{input.id}"

    if not local_storage.exists(filename):
        local_storage.save(filename, storage.open(input.path))

    return local_storage.path(filename)


@dataclass
class UploadVideoToYouTubeInput:
    title: str
    description: str
    file_path: str
    tags: list[str]

    @property
    def tags_as_str(self) -> list[str]:
        return ",".join(self.tags)


@activity.defn
async def upload_video_to_youtube(input: UploadVideoToYouTubeInput):
    async for response in youtube_videos_insert(
        title=input.title,
        description=input.description,
        tags=input.tags_as_str,
        file_path=input.file_path,
    ):
        activity.heartbeat("video uploading")

    return response


@dataclass
class ExtractVideoThumbnailInput:
    file_path: str
    schedule_item_id: int


@activity.defn
async def extract_video_thumbnail(input: ExtractVideoThumbnailInput):
    thumbnail_file_name = f"{input.schedule_item_id}-thumbnail.jpg"
    file_path = local_storage.path(thumbnail_file_name)

    if local_storage.exists(thumbnail_file_name):
        return file_path

    video_capture = cv2.VideoCapture(input.file_path)
    success, image = video_capture.read()

    if not success:
        raise ValueError("Unable to extract frame")

    cv2.imwrite(file_path, image)
    return file_path


@dataclass
class SetThumbnailToYouTubeVideoInput:
    youtube_id: str
    thumbnail_path: str


@activity.defn
async def set_thumbnail_to_youtube_video(input: SetThumbnailToYouTubeVideoInput):
    return await youtube_videos_set_thumbnail(
        video_id=input.youtube_id,
        thumbnail_path=input.thumbnail_path,
    )


@activity.defn
async def cleanup_local_video_files(schedule_item_id: int):
    local_storage.delete(f"{schedule_item_id}-thumbnail.jpg")
    local_storage.delete(f"yt_upload_{schedule_item_id}")
