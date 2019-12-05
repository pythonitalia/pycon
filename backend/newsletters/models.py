from django.db import models
from django.utils.translation import ugettext_lazy as _


class Subscription(models.Model):
    email = models.EmailField(_("email address"), unique=True)
    date_subscribed = models.DateTimeField(_("date subscribed"), auto_now_add=True)

    def __str__(self):
        return f"{self.email} subscribed on {self.date_subscribed}"
