from django.db import models


class PrivacyPolicyAcceptanceRecord(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.PROTECT)
    accepted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    privacy_policy = models.CharField(max_length=1024)
