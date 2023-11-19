from dataclasses import dataclass
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from video_upload.workflows.upload_schedule_item_video import (
        UploadScheduleItemVideoWorkflow,
    )


@dataclass
class BatchMultipleScheduleItemsVideoUploadInput:
    schedule_items_ids: list


@workflow.defn
class BatchMultipleScheduleItemsVideoUpload:
    input = BatchMultipleScheduleItemsVideoUploadInput

    @workflow.run
    async def run(self, input: BatchMultipleScheduleItemsVideoUploadInput):
        for schedule_item_id in input.schedule_items_ids:
            await workflow.execute_child_workflow(
                UploadScheduleItemVideoWorkflow,
                UploadScheduleItemVideoWorkflow.input(
                    schedule_item_id=schedule_item_id
                ),
                id=f"upload_schedule_item_video_{schedule_item_id}",
            )
