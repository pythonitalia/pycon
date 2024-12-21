from conferences.querysets import ConferenceQuerySetMixin
from django.db import models


class InvitationLetterRequestQuerySet(ConferenceQuerySetMixin, models.QuerySet):
    def not_processed(self):
        from visa.models import InvitationLetterRequestStatus

        return self.filter(
            status__in=[
                InvitationLetterRequestStatus.PENDING,
                InvitationLetterRequestStatus.FAILED_TO_GENERATE,
            ]
        )

    def not_processing(self):
        from visa.models import InvitationLetterRequestStatus

        return self.exclude(status__in=[InvitationLetterRequestStatus.PROCESSING])
