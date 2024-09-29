from django.db import models
from typing import TYPE_CHECKING

from conferences.querysets import ConferenceQuerySetMixin

if TYPE_CHECKING:
    from notifications.models import EmailTemplate


class EmailTemplateQuerySet(ConferenceQuerySetMixin, models.QuerySet):
    def get_by_identifier(
        self, identifier: "EmailTemplate.Identifier"
    ) -> "EmailTemplate":
        return self.get(identifier=identifier)

    def system_templates(self):
        return self.filter(is_system_template=True)


class SentEmailQuerySet(ConferenceQuerySetMixin, models.QuerySet):
    def pending(self):
        return self.filter(status=self.model.Status.pending)

    def get_by_message_id(self, message_id):
        return self.get(message_id=message_id)
