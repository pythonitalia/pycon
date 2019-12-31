from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices


class Subscription(models.Model):
    email = models.EmailField(_("email address"), unique=True)
    date_subscribed = models.DateTimeField(_("date subscribed"), auto_now_add=True)

    def __str__(self):
        return f"{self.email} subscribed on {self.date_subscribed}"


RECIPIENTS_TYPES = Choices(
    ("newsletter", _("Newsletter")),
    # ("other", _("Other")),
)


class Email(models.Model):
    subject = models.CharField(_("subject"), max_length=100)
    heading = models.CharField(_("heading"), max_length=300)
    body = models.TextField(_("body"))
    cta_label = models.CharField(
        _("link label"), max_length=100, blank=True, default=""
    )
    cta_link = models.CharField(_("link"), max_length=100, blank=True, default="")
    recipients_types = models.CharField(
        _("Recipients Type"), choices=RECIPIENTS_TYPES, max_length=50
    )
    # Recipients is a read-only field only to send the final recipients
    recipients = models.TextField(_("recipients"), blank=True, default="")
    scheduled_date = models.DateTimeField(_("scheduled date"), null=True)
