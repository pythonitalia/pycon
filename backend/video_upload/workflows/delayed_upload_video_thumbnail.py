import asyncio
from dataclasses import dataclass
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from video_upload.activities import (
        set_thumbnail_to_youtube_video,
        SetThumbnailToYouTubeVideoInput,
        CleanupLocalVideoFilesInput,
        cleanup_local_video_files,
    )


@dataclass
class DelayedUploadVideoThumbnailInput:
    schedule_item_id: int
    youtube_id: int
    thumbnail_path: str


@workflow.defn
class DelayedUploadVideoThumbnail:
    input = DelayedUploadVideoThumbnailInput

    @workflow.run
    async def run(self, input: DelayedUploadVideoThumbnailInput):
        # sleep for 12 hours at the start
        await asyncio.sleep(12 * 60 * 60)
        await workflow.execute_activity(
            set_thumbnail_to_youtube_video,
            SetThumbnailToYouTubeVideoInput(
                youtube_id=input.youtube_id,
                thumbnail_path=input.thumbnail_path,
            ),
            schedule_to_close_timeout=timedelta(minutes=1),
            retry_policy=RetryPolicy(
                maximum_attempts=6,
                backoff_coefficient=12 * 60 * 60,
            ),
        )

        await workflow.execute_activity(
            cleanup_local_video_files,
            CleanupLocalVideoFilesInput(
                schedule_item_id=input.schedule_item_id,
                delete_thumbnail=True,
            ),
            start_to_close_timeout=timedelta(seconds=30),
        )
