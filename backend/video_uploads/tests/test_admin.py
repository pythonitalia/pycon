import pytest
from video_uploads.models import WetransferToS3TransferRequest
from video_uploads.admin import queue_wetransfer_to_s3_transfer_request, retry_transfer
from video_uploads.tests.factories import WetransferToS3TransferRequestFactory

pytestmark = pytest.mark.django_db


def test_queue_wetransfer_to_s3_transfer_request(
    mocker, django_capture_on_commit_callbacks
):
    mock_process_wetransfer_to_s3_transfer_request = mocker.patch(
        "video_uploads.admin.process_wetransfer_to_s3_transfer_request"
    )
    mock_launch_heavy_processing_worker = mocker.patch(
        "video_uploads.admin.launch_heavy_processing_worker"
    )

    request = WetransferToS3TransferRequestFactory()

    with django_capture_on_commit_callbacks(execute=True):
        queue_wetransfer_to_s3_transfer_request(request)

    request.refresh_from_db()

    assert request.status == WetransferToS3TransferRequest.Status.QUEUED
    assert request.failed_reason == ""

    mock_process_wetransfer_to_s3_transfer_request.apply_async.assert_called_once_with(
        args=[request.id], queue="heavy_processing"
    )
    mock_launch_heavy_processing_worker.delay.assert_called_once()


def test_retry_transfer():
    obj1, obj2 = WetransferToS3TransferRequestFactory.create_batch(2)
    retry_transfer(None, None, WetransferToS3TransferRequest.objects.all())

    obj1.refresh_from_db()
    obj2.refresh_from_db()

    assert obj1.status == WetransferToS3TransferRequest.Status.QUEUED
    assert obj2.status == WetransferToS3TransferRequest.Status.QUEUED
