from conferences.querysets import ConferenceQuerySetMixin
from django.db import models


class InvitationLetterRequestQuerySet(ConferenceQuerySetMixin, models.QuerySet):
    def of_user(self, user):
        return self.filter(requester=user)
