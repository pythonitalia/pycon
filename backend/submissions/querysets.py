from api.helpers.ids import decode_hashid
from conferences.querysets import ConferenceQuerySetMixin
from django.db import models
from ordered_model.models import OrderedModelQuerySet


class SubmissionQuerySet(ConferenceQuerySetMixin, models.QuerySet):
    def get_by_hashid(self, hashid):
        return self.get(pk=decode_hashid(hashid))

    def non_cancelled(self):
        return self.filter(status__in=self.model.NON_CANCELLED_STATUSES)

    def accepted(self):
        return self.filter(status=self.model.STATUS.accepted)

    def of_user(self, user):
        return self.filter(speaker=user)


class ProposalCoSpeakerQuerySet(
    ConferenceQuerySetMixin, OrderedModelQuerySet, models.QuerySet
):
    def accepted(self):
        from submissions.models import ProposalCoSpeakerStatus

        return self.filter(status=ProposalCoSpeakerStatus.accepted)
