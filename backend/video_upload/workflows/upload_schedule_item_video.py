from dataclasses import dataclass
from datetime import timedelta
from temporalio import workflow
from temporalio.exceptions import ActivityError
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from video_upload.activities import fetch_schedule_item, download_video_file
    from video_upload.activities import (
        upload_video_to_youtube,
        add_youtube_id_to_schedule_item,
        fetch_speakers_data,
        UploadVideoToYouTubeInput,
        extract_video_thumbnail,
        set_thumbnail_to_youtube_video,
        SetThumbnailToYouTubeVideoInput,
        cleanup_local_video_files,
        CleanupLocalVideoFilesInput,
    )
    from video_upload.workflows.delayed_upload_video_thumbnail import (
        DelayedUploadVideoThumbnail,
    )
    from video_upload.activities import (
        AddYouTubeIDToScheduleItemInput,
        ExtractVideoThumbnailInput,
    )
    from video_upload.activities import ScheduleItemData
    from video_upload.activities import DownloadVideoFileInput


@dataclass
class UploadScheduleItemVideoWorkflowInput:
    schedule_item_id: int


@workflow.defn
class UploadScheduleItemVideoWorkflow:
    input = UploadScheduleItemVideoWorkflowInput

    @workflow.run
    async def run(self, input: UploadScheduleItemVideoWorkflowInput):
        schedule_item = await workflow.execute_activity(
            fetch_schedule_item,
            input.schedule_item_id,
            schedule_to_close_timeout=timedelta(seconds=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
            ),
        )

        speakers_data = await workflow.execute_activity(
            fetch_speakers_data,
            schedule_item.speakers_ids,
            schedule_to_close_timeout=timedelta(seconds=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
            ),
        )

        media_file_path = await workflow.execute_activity(
            download_video_file,
            DownloadVideoFileInput(
                path=schedule_item.video_uploaded_path,
                id=schedule_item.id,
            ),
            schedule_to_close_timeout=timedelta(minutes=20),
            retry_policy=RetryPolicy(
                maximum_attempts=1, non_retryable_error_types=["ResourceNotFoundError"]
            ),
        )

        upload_video_input = self.create_youtube_video_input(
            schedule_item=schedule_item,
            speakers_data=speakers_data,
            media_file_path=media_file_path,
        )

        if len(upload_video_input.title) > 100:
            raise ValueError("YouTube title is too long")

        if len(upload_video_input.description) > 5000:
            raise ValueError("YouTube description is too long")

        response = await workflow.execute_activity(
            upload_video_to_youtube,
            upload_video_input,
            schedule_to_close_timeout=timedelta(minutes=30),
            retry_policy=RetryPolicy(
                maximum_attempts=1,
            ),
        )

        await workflow.execute_activity(
            add_youtube_id_to_schedule_item,
            AddYouTubeIDToScheduleItemInput(
                schedule_item_id=schedule_item.id, youtube_id=response["id"]
            ),
            schedule_to_close_timeout=timedelta(seconds=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
            ),
        )

        thumbnail_path = await workflow.execute_activity(
            extract_video_thumbnail,
            ExtractVideoThumbnailInput(
                file_path=media_file_path,
                schedule_item_id=schedule_item.id,
            ),
            schedule_to_close_timeout=timedelta(minutes=20),
            retry_policy=RetryPolicy(
                maximum_attempts=30,
                backoff_coefficient=1,
            ),
        )

        delete_thumbnail = True
        try:
            await workflow.execute_activity(
                set_thumbnail_to_youtube_video,
                SetThumbnailToYouTubeVideoInput(
                    youtube_id=response["id"],
                    thumbnail_path=thumbnail_path,
                ),
                schedule_to_close_timeout=timedelta(minutes=1),
                retry_policy=RetryPolicy(
                    maximum_attempts=1,
                    backoff_coefficient=2.0,
                ),
            )
        except ActivityError as exc:
            if exc.cause == "DailyThumbnailLimitException":
                workflow.start_child_workflow(
                    DelayedUploadVideoThumbnail.run,
                    DelayedUploadVideoThumbnail.input(
                        schedule_item_id=schedule_item.id,
                        youtube_id=response["id"],
                        thumbnail_path=thumbnail_path,
                    ),
                    id=f"upload_video_thumbnail-{schedule_item.id}",
                )
                delete_thumbnail = False
            else:
                raise

        await workflow.execute_activity(
            cleanup_local_video_files,
            CleanupLocalVideoFilesInput(
                schedule_item_id=schedule_item.id, delete_thumbnail=delete_thumbnail
            ),
            start_to_close_timeout=timedelta(seconds=30),
        )

    def create_youtube_video_input(
        self,
        *,
        schedule_item: ScheduleItemData,
        speakers_data: dict,
        media_file_path: str,
    ) -> UploadVideoToYouTubeInput:
        count_speakers = len(schedule_item.speakers_ids)
        speakers_names = ", ".join(
            [
                speakers_data[str(speaker_id)]["fullname"]
                for speaker_id in schedule_item.speakers_ids
            ]
        )

        if count_speakers == 0 or count_speakers > 2:
            title = f"{schedule_item.title} - {schedule_item.conference_name}"
        else:
            title = f"{schedule_item.title} - {speakers_names}"

        if len(title) > 100:
            title = schedule_item.title

        description = (
            f"{schedule_item.title} - "
            f"{speakers_names} - {schedule_item.conference_name}\n\n"
        )

        if schedule_item.elevator_pitch:
            description += f"{schedule_item.elevator_pitch}\n\n"
        elif schedule_item.description:
            description += f"{schedule_item.description}\n\n"
        elif schedule_item.keynote_description:
            description += f"{schedule_item.keynote_description}\n\n"

        if schedule_item.type.lower() != "custom":
            description += (
                f"Full Abstract: https://2023.pycon.it/event/{schedule_item.slug}\n\n"
            )

        description += f"{schedule_item.conference_youtube_video_bottom_text}\n\n"

        if schedule_item.clean_tags:
            description += " ".join(schedule_item.hashtags)

        return UploadVideoToYouTubeInput(
            title=replace_invalid_chars_with_lookalikes(title),
            description=replace_invalid_chars_with_lookalikes(description),
            file_path=media_file_path,
            tags=schedule_item.clean_tags,
        )


def replace_invalid_chars_with_lookalikes(text: str) -> str:
    homoglyphs = {
        "<": "\u1438",
        ">": "\u1433",
    }
    for char, homoglyph in homoglyphs.items():
        text = text.replace(char, homoglyph)
    return text
