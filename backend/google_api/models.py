from typing import Optional
from zoneinfo import ZoneInfo
from django.db import models
from django.db.models import F
from django.db.models.functions import Coalesce
from django.conf import settings
from django.utils import timezone

DAILY_YOUTUBE_QUOTA = 10_000


class GoogleCloudOAuthCredentialQuerySet(models.QuerySet):
    async def get_by_client_id(self, client_id: str) -> "GoogleCloudOAuthCredential":
        return await self.filter(client_id=client_id).afirst()


class GoogleCloudOAuthCredential(models.Model):
    client_id = models.TextField()
    client_secret = models.TextField()
    project_id = models.TextField()
    auth_uri = models.URLField()
    token_uri = models.URLField()
    auth_provider_x509_cert_url = models.URLField()

    quota_limit_for_youtube = models.IntegerField(default=DAILY_YOUTUBE_QUOTA)

    objects = GoogleCloudOAuthCredentialQuerySet.as_manager()

    @staticmethod
    async def get_available_credentials_token(
        service: str, min_quota: int
    ) -> Optional["GoogleCloudToken"]:
        midnight_pacific_time = (
            timezone.now()
            .astimezone(ZoneInfo("America/Los_Angeles"))
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .astimezone(ZoneInfo("UTC"))
        )

        field_name = f"quota_limit_for_{service}"

        credential = (
            await GoogleCloudOAuthCredential.objects.annotate(
                used_quota=Coalesce(
                    models.Sum(
                        "usedrequestquota__cost",
                        # filter by quota used after midnight
                        filter=models.Q(
                            usedrequestquota__service=service,
                            usedrequestquota__used_at__gte=midnight_pacific_time,
                        ),
                    ),
                    0,
                ),
                quota_left=Coalesce(
                    F(field_name) - F("used_quota"),
                    0,
                ),
                has_token=models.Exists(
                    GoogleCloudToken.objects.filter(
                        oauth_credential_id=models.OuterRef("id")
                    )
                ),
            )
            .filter(quota_left__gte=min_quota, has_token=True)
            .order_by("quota_left")
            .afirst()
        )
        return (await credential.googlecloudtoken_set.afirst()) if credential else None

    class Meta:
        verbose_name = "Google Cloud OAuth Credential"
        verbose_name_plural = "Google Cloud OAuth Credentials"


class UsedRequestQuota(models.Model):
    used_at = models.DateTimeField(auto_now_add=True)
    credentials = models.ForeignKey(
        GoogleCloudOAuthCredential, on_delete=models.CASCADE
    )
    cost = models.IntegerField()
    service = models.CharField(max_length=255)


class GoogleCloudToken(models.Model):
    oauth_credential = models.ForeignKey(
        GoogleCloudOAuthCredential, on_delete=models.CASCADE
    )
    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.TextField()
    refresh_token = models.TextField()
    token_uri = models.URLField()
    client_id = models.TextField()
    client_secret = models.TextField()
    scopes = models.TextField()
