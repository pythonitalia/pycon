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

    def system(self):
        return self.filter(is_system_template=True)


class SentEmailQuerySet(ConferenceQuerySetMixin, models.QuerySet):
    def pending(self):
        return self.filter(status=self.model.Status.pending)

    def for_recipient(self, user):
        return self.filter(recipient=user)

    def for_template(self, identifier: "EmailTemplate.Identifier"):
        return self.filter(email_template__identifier=identifier)

    def get_by_message_id(self, message_id):
        return self.filter(message_id=message_id).first()
