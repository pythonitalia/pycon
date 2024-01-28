from api.helpers.ids import decode_hashid
from django.db import models


class SubmissionManager(models.Manager):
    def for_conference(self, conference):
        return self.filter(conference=conference)

    def get_by_hashid(self, hashid):
        return self.get(pk=decode_hashid(hashid))

    def non_cancelled(self):
        return self.filter(status__in=self.model.NON_CANCELLED_STATUSES)
