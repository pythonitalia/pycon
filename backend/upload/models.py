from django.db import models
from django.utils.translation import ugettext_lazy as _


class Upload(models.Model):
    file = models.FileField(_("file"), upload_to="tmp", blank=False, null=False)
    date_upload = models.DateTimeField(_("date upload"), auto_now_add=True)

    def __str__(self):
        return self.file.name
