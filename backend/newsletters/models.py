from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from notifications.emails import send_mail


class Subscription(models.Model):
    email = models.EmailField(_("email address"), unique=True)
    date_subscribed = models.DateTimeField(_("date subscribed"), auto_now_add=True)

    def __str__(self):
        return f"{self.email} subscribed on {self.date_subscribed}"


class Email(models.Model):

    RECIPIENTS_TYPES = Choices(
        ("newsletter", _("Newsletter")),
        # ("other", _("Other")),
    )

    subject = models.CharField(_("subject"), max_length=100)
    heading = models.CharField(_("heading"), max_length=300)
    body = models.TextField(_("body"))
    cta_label = models.CharField(
        _("link label"), max_length=100, blank=True, default=""
    )
    cta_link = models.CharField(_("link"), max_length=100, blank=True, default="")
    recipients_type = models.CharField(
        _("Recipients Type"), choices=RECIPIENTS_TYPES, max_length=50
    )
    # Recipients is a read-only field only to send the final recipients
    recipients = ArrayField(models.EmailField(_("recipients")), blank=True, null=True)
    scheduled_date = models.DateTimeField(_("scheduled date"), null=True)

    def __str__(self):
        return f"{self.subject}"

    def set_recipients(self):
        # if email.recipients_type == "newsletter":
        self.recipients = [
            subscription.email for subscription in Subscription.objects.all()
        ]

    def send_email(self):
        self.set_recipients()

        resp = (
            send_mail(
                self.subject,
                self.recipients,
                "newsletter",
                context=self.__dict__,
                path="emails/newsletters/",
            )
            == 1
        )

        self.save()

        return resp
