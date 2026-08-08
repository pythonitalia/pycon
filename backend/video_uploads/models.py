from model_utils.models import TimeStampedModel
from django.db import models


class VideosImportRequest(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending"
        QUEUED = "queued"
        PROCESSING = "processing"
        FAILED = "failed"
        DONE = "done"

    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name="conference",
    )
    source_url = models.URLField("Source URL", max_length=2048)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    imported_files = models.JSONField("Imported files", blank=True, null=True)
    failed_reason = models.TextField("Failed reason", blank=True, null=True)

    started_at = models.DateTimeField("Started at", blank=True, null=True)
    finished_at = models.DateTimeField("Finished at", blank=True, null=True)
