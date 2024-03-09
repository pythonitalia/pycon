from dataclasses import dataclass
import cv2
from django.core.files.base import ContentFile
from django.core.files.storage import storages
from schedule.models import ScheduleItem

from jinja2 import Environment

local_storage = storages["localstorage"]


@dataclass
class VideoInfo:
    title: str
    description: str
    tags: list[str]

    @property
    def tags_as_str(self) -> str:
        return ",".join(self.tags)


def create_video_info(schedule_item: ScheduleItem) -> VideoInfo:
    all_speakers = schedule_item.speakers
    count_speakers = len(all_speakers)
    speakers_names = ", ".join([speaker.fullname for speaker in all_speakers])
    tags = [
        clean_tag(tag)
        for tag in (
            schedule_item.submission.tags.values_list("name", flat=True)
            if schedule_item.submission_id
            else []
        )
    ]

    context = {
        "has_speakers": count_speakers > 0,
        "has_more_than_2_speakers": count_speakers > 2,
        "has_zero_or_more_than_2_speakers": count_speakers == 0 or count_speakers > 2,
        "count_speakers": count_speakers,
        "speakers_names": speakers_names,
        "title": schedule_item.title,
        "abstract": schedule_item.abstract,
        "elevator_pitch": schedule_item.elevator_pitch,
        "conference_name": schedule_item.conference.name.localize("en"),
        "hashtags": " ".join([f"#{tag}" for tag in tags]),
    }

    title = _process_string_template(
        schedule_item.conference.video_title_template, context
    )

    if len(title) > 100:
        title = schedule_item.title

    description = _process_string_template(
        schedule_item.conference.video_description_template, context
    )

    return VideoInfo(
        title=replace_invalid_chars_with_lookalikes(title),
        description=replace_invalid_chars_with_lookalikes(description),
        tags=tags,
    )


def _process_string_template(template_string: str, context) -> str:
    env = Environment(
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.from_string(template_string)
    return template.render(context).strip().replace("\n\n\n", "\n\n")


def download_video_file(id: int, path: str) -> str:
    storage = storages["conferencevideos"]
    filename = get_video_file_name(id)

    if not local_storage.exists(filename):
        local_storage.save(filename, storage.open(path))

    return local_storage.path(filename)


def extract_video_thumbnail(remote_video_path: str, id: int) -> str:
    thumbnail_file_name = get_thumbnail_file_name(id)
    file_path = local_storage.path(thumbnail_file_name)

    if local_storage.exists(thumbnail_file_name):
        return file_path

    local_video_path = download_video_file(id, remote_video_path)

    video_capture = cv2.VideoCapture(local_video_path)
    success, image = video_capture.read()

    if not success:
        raise ValueError("Unable to extract frame")

    ret, buffer = cv2.imencode(".jpg", image)
    if not ret:
        raise ValueError("Unable to encode frame")

    content_file = ContentFile(buffer.tobytes())
    local_storage.save(thumbnail_file_name, content_file)
    return thumbnail_file_name


def cleanup_local_files(id: int, delete_thumbnail: bool = True):
    thumbnail_file_name = get_thumbnail_file_name(id)
    if delete_thumbnail and local_storage.exists(thumbnail_file_name):
        local_storage.delete(thumbnail_file_name)

    video_file_name = get_video_file_name(id)
    if local_storage.exists(video_file_name):
        local_storage.delete(video_file_name)


def get_thumbnail_file_name(id: int) -> str:
    return f"{id}-thumbnail.jpg"


def get_video_file_name(id: int) -> str:
    return f"{id}-video_upload"


def replace_invalid_chars_with_lookalikes(text: str) -> str:
    homoglyphs = {
        "<": "\u1438",
        ">": "\u1433",
    }
    for char, homoglyph in homoglyphs.items():
        text = text.replace(char, homoglyph)
    return text


def clean_tag(tag: str) -> str:
    return tag.strip().replace(" ", "").replace("-", "").replace(".", "")
