import logging

from django.utils import timezone
from django.db import transaction

from video_uploads.transfer import WetransferProcessing
from video_uploads.models import VideosImportRequest
from pycon.celery import app
from pycon.celery_utils import OnlyOneAtTimeTask


logger = logging.getLogger(__name__)


@app.task(base=OnlyOneAtTimeTask)
def process_videos_import_request(request_id):
    with transaction.atomic():
        videos_import_request = VideosImportRequest.objects.select_for_update().get(
            id=request_id
        )

        if videos_import_request.status != VideosImportRequest.Status.QUEUED:
            logger.warning(
                "VideosImportRequest with id=%s is not in QUEUED status, skipping",
                request_id,
            )
            return

        videos_import_request.status = VideosImportRequest.Status.PROCESSING
        videos_import_request.started_at = timezone.now()
        videos_import_request.save(update_fields=["status", "started_at"])

    videos_import_request = VideosImportRequest.objects.get(id=request_id)

    try:
        processing = WetransferProcessing(videos_import_request)
        imported_files = processing.run()

        videos_import_request.status = VideosImportRequest.Status.DONE
        videos_import_request.imported_files = imported_files
        videos_import_request.finished_at = timezone.now()
        videos_import_request.save(
            update_fields=["status", "imported_files", "finished_at"]
        )
    except Exception as e:
        logger.exception("Error processing videos import request: %s", e)
        videos_import_request.status = VideosImportRequest.Status.FAILED
        videos_import_request.failed_reason = str(e)
        videos_import_request.save(update_fields=["status", "failed_reason"])
