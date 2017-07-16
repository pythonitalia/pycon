"""Association model."""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import MembershipManager


class Membership(models.Model):
    """Application of a member."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    date = models.DateField(auto_now_add=True)

    objects = MembershipManager()

    def __str__(self):
        return f"{self.user.email} - {self.date.year}"

    class Meta:
        verbose_name = _("Membership")
        verbose_name_plural = _("Memberships")
