from conferences.querysets import ConferenceQuerySetMixin
from django.db import models


class InvitationLetterRequestQuerySet(ConferenceQuerySetMixin, models.QuerySet):
    ...
