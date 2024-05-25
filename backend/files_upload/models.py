from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel


def get_upload_to(purpose, id):
    return f"files/{purpose}/{id}"


def get_upload_to_from_instance(instance, filename):
    return get_upload_to_from_instance(instance.purpose, instance.id)


class File(UUIDModel, TimeStampedModel):
    class Purpose(models.TextChoices):
        PARTICIPANT_AVATAR = "participant_avatar", "Participant Avatar"
        PROPOSAL_RESOURCE = "proposal_resource", "Proposal Resource"

    file = models.FileField(
        "File",
        upload_to=get_upload_to_from_instance,
        null=True,
        blank=True,
    )
    uploaded_by = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    purpose = models.CharField(
        "Purpose",
        max_length=32,
        choices=Purpose.choices,
    )

    def create_upload_url(self):
        return self.file.storage.generate_upload_url(self.file)
