import logging

from django.utils import timezone
from django.db import transaction

from video_uploads.transfer import WetransferProcessing
from video_uploads.models import WetransferToS3TransferRequest
from pycon.celery import app
from pycon.celery_utils import OnlyOneAtTimeTask


logger = logging.getLogger(__name__)


@app.task(base=OnlyOneAtTimeTask)
def process_wetransfer_to_s3_transfer_request(request_id):
    with transaction.atomic():
        wetransfer_to_s3_transfer_request = (
            WetransferToS3TransferRequest.objects.select_for_update().get(id=request_id)
        )

        if (
            wetransfer_to_s3_transfer_request.status
            != WetransferToS3TransferRequest.Status.QUEUED
        ):
            logger.warn(
                "WetransferToS3TransferRequest with id=%s is not in QUEUED status, skipping",
                request_id,
            )
            return

        wetransfer_to_s3_transfer_request.status = (
            WetransferToS3TransferRequest.Status.PROCESSING
        )
        wetransfer_to_s3_transfer_request.started_at = timezone.now()
        wetransfer_to_s3_transfer_request.save(update_fields=["status", "started_at"])

    wetransfer_to_s3_transfer_request = WetransferToS3TransferRequest.objects.get(
        id=request_id
    )

    try:
        processing = WetransferProcessing(wetransfer_to_s3_transfer_request)
        imported_files = processing.run()

        wetransfer_to_s3_transfer_request.status = (
            WetransferToS3TransferRequest.Status.DONE
        )
        wetransfer_to_s3_transfer_request.imported_files = imported_files
        wetransfer_to_s3_transfer_request.finished_at = timezone.now()
        wetransfer_to_s3_transfer_request.save(
            update_fields=["status", "imported_files", "finished_at"]
        )
    except Exception as e:
        logger.exception("Error processing wetransfer to s3 transfer request: %s", e)
        wetransfer_to_s3_transfer_request.status = (
            WetransferToS3TransferRequest.Status.FAILED
        )
        wetransfer_to_s3_transfer_request.failed_reason = str(e)
        wetransfer_to_s3_transfer_request.save(
            update_fields=["status", "failed_reason"]
        )
