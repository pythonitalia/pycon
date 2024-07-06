from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel


def get_upload_to(type, id, filename):
    ext = filename.split(".")[-1]
    return f"files/{type}/{id}.{ext}"


def get_upload_to_from_instance(instance, filename):
    return get_upload_to(instance.type, instance.id, filename)


class File(UUIDModel, TimeStampedModel):
    class Type(models.TextChoices):
        PARTICIPANT_AVATAR = "participant_avatar", "Participant Avatar"
        PROPOSAL_MATERIAL = "proposal_material", "Proposal Material"

    file = models.FileField(
        "File",
        upload_to=get_upload_to_from_instance,
        null=False,
        blank=False,
    )
    uploaded_by = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    type = models.CharField(
        "Type",
        max_length=32,
        choices=Type.choices,
    )
    virus = models.BooleanField(
        "Is virus",
        null=True,
        blank=True,
    )
    mime_type = models.CharField(
        "Mime Type",
        max_length=255,
        null=True,
        blank=True,
    )

    def create_upload_url(self) -> str:
        return self.file.storage.generate_upload_url(self)

    @property
    def url(self) -> str:
        return self.file.url

    @property
    def is_public(self) -> bool:
        return True
