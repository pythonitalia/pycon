from dataclasses import dataclass
from datetime import timedelta
from temporalio import workflow
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
                maximum_attempts=3,
            ),
        )

        await workflow.execute_activity(
            set_thumbnail_to_youtube_video,
            SetThumbnailToYouTubeVideoInput(
                youtube_id=response["id"],
                thumbnail_path=thumbnail_path,
            ),
            schedule_to_close_timeout=timedelta(minutes=20),
            retry_policy=RetryPolicy(
                maximum_attempts=5,
                backoff_coefficient=2.0,
            ),
        )

        await workflow.execute_activity(
            cleanup_local_video_files,
            schedule_item.id,
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

        if count_speakers >= 3 or not schedule_item.has_submission:
            title = f"{schedule_item.title} - {schedule_item.conference_name}"
        else:
            title = f"{schedule_item.title} - {speakers_names}"

        description = f"{schedule_item.title} - {schedule_item.conference_name}\n\n"

        if schedule_item.elevator_pitch:
            description += f"{schedule_item.elevator_pitch}\n\n"
        elif schedule_item.description:
            description += f"{schedule_item.description}\n\n"

        if schedule_item.type.lower() != "custom":
            description += (
                f"Full Abstract: https://2023.pycon.it/event/{schedule_item.slug}\n"
            )

        if count_speakers:
            description += f"Speakers: {speakers_names}\n\n"

        description += schedule_item.conference_youtube_video_bottom_text

        return UploadVideoToYouTubeInput(
            title=title,
            description=description,
            file_path=media_file_path,
            tags=schedule_item.tags,
        )