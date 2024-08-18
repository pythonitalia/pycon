from django.db import models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from notifications.models import EmailTemplate


class EmailTemplateQuerySet(models.QuerySet):
    def get_by_identifier(
        self, identifier: "EmailTemplate.Identifier"
    ) -> "EmailTemplate":
        return self.get(identifier=identifier)


class SentEmailQuerySet(models.QuerySet):
    def pending(self):
        return self.filter(status=self.model.Status.pending)
