from api.helpers.ids import decode_hashid
from conferences.querysets import ConferenceQuerySetMixin
from django.db import models


class SubmissionQuerySet(ConferenceQuerySetMixin, models.QuerySet):
    def get_by_hashid(self, hashid):
        return self.get(pk=decode_hashid(hashid))

    def non_cancelled(self):
        return self.filter(status__in=self.model.NON_CANCELLED_STATUSES)

    def accepted(self):
        return self.filter(status=self.model.STATUS.accepted)
