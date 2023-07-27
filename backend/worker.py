import os
import asyncio
from django.apps import apps
from django.conf import settings
from temporalio.client import Client
from temporalio.worker import Worker


async def main():
    apps.populate(settings.INSTALLED_APPS)

    from video_upload.activities import (
        fetch_schedule_item,
        download_video_file,
        upload_video_to_youtube,
        fetch_speakers_data,
        add_youtube_id_to_schedule_item,
        extract_video_thumbnail,
        set_thumbnail_to_youtube_video,
    )
    from video_upload.workflows.upload_schedule_item_video import (
        UploadScheduleItemVideoWorkflow,
    )

    client = await Client.connect(os.getenv("TEMPORAL_ADDRESS"))
    worker = Worker(
        client,
        task_queue="default",
        workflows=[UploadScheduleItemVideoWorkflow],
        activities=[
            fetch_schedule_item,
            download_video_file,
            upload_video_to_youtube,
            fetch_speakers_data,
            add_youtube_id_to_schedule_item,
            extract_video_thumbnail,
            set_thumbnail_to_youtube_video,
        ],
    )
    print("Starting worker")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
