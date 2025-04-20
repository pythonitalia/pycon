import logging
from django.conf import settings
from django.db import models
import httpx
from model_utils.models import TimeStampedModel
from colorfield.fields import ColorField
from django.db import transaction


logger = logging.getLogger(__name__)


class Community(TimeStampedModel):
    name = models.CharField(max_length=300)
    hostname = models.CharField(max_length=256)
    description = models.TextField()

    landing_page_primary_color = ColorField(
        blank=True,
        null=True,
        help_text=(
            "Used for the background of the landing page. "
            "Depending on the contrast, it will be used to decide if "
            "the text should be white or black."
        ),
    )
    landing_page_secondary_color = ColorField(
        blank=True,
        null=True,
        help_text=(
            "Used for the logo color, borders "
            "and, if not specified, the hover effect of the links."
        ),
    )
    landing_page_hover_color = ColorField(
        blank=True,
        null=True,
        help_text="Optional. Used when hovering the links. If empty, it will use the secondary color.",
    )
    landing_page_custom_logo_svg = models.TextField(
        blank=True,
        null=True,
        help_text=(
            "Optional. If empty, it will use the Python Italia logo with the community name below. "
            "Copy your SVG code here."
        ),
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        transaction.on_commit(self.revalidate_landing_page)

    def revalidate_landing_page(self):
        # this is very bad :)
        try:
            for _ in range(3):
                response = httpx.post(
                    f"https://{self.hostname}/api/revalidate/",
                    json={
                        "path": f"/{self.hostname}",
                        "secret": settings.REVALIDATE_SECRET,
                    },
                )

                if response.status_code == 200:
                    break

            response.raise_for_status()
        except Exception as e:
            logger.exception("Error while revalidating landing page", exc_info=e)
            pass

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Communities"


class CommunityMember(TimeStampedModel):
    class Role(models.TextChoices):
        ADMIN = "ADMIN"

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="community_memberships"
    )
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name="members"
    )
    role = models.CharField(choices=Role.choices, default=Role.ADMIN, max_length=300)


class Link(TimeStampedModel):
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name="links"
    )
    url = models.URLField()
    label = models.CharField(max_length=300)

    def __str__(self) -> str:
        return f"{self.label} - {self.url}"
