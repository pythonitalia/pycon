from api.helpers.ids import decode_hashid
from django.db import models


class SubmissionManager(models.Manager):
    def get_by_hashid(self, hashid):
        return self.get(pk=decode_hashid(hashid))
