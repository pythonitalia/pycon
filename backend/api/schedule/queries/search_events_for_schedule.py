import strawberry
from django.db.models import Q, QuerySet
from strawberry_django.optimizer import OptimizerStore, optimize

from api.conferences.types import Keynote
from api.context import Info
from api.permissions import CanEditSchedule
from api.submissions.types import Submission
from conferences.models import Keynote as KeynoteModel
from participants import models as participant_models
from submissions.models import Submission as SubmissionModel


@strawberry.type
class SearchEventsForScheduleResult:
    conference_id: strawberry.Private[int]
    proposals: strawberry.Private[QuerySet[SubmissionModel]]
    keynotes: strawberry.Private[QuerySet[KeynoteModel]]

    @strawberry.field
    def results(self, info: Info) -> list[Submission | Keynote]:
        # Participant deliberately has no reverse User relation, so batch the
        # speakers from both sides of the union into the shared request cache.
        participants = participant_models.Participant.objects.filter(
            conference_id=self.conference_id,
        ).filter(
            Q(user_id__in=self.proposals.values("speaker_id"))
            | Q(user_id__in=self.keynotes.values("speakers__user_id"))
        )
        participants_by_conference = info.context._participants_data
        if participants_by_conference is None:
            participants_by_conference = {}
            info.context._participants_data = participants_by_conference

        participants_data = participants_by_conference.setdefault(
            self.conference_id, {}
        )
        participants_data.update(
            {participant.user_id: participant for participant in participants}
        )

        # The mixed union has to become a list here, so optimize each queryset
        # before Strawberry loses the opportunity to inspect its model type.
        # Keep title explicit because the frontend selects its resolver twice
        # under different aliases.
        return [
            *optimize(
                self.proposals,
                info,
                store=OptimizerStore.with_hints(only=["title"]),
            ),
            *optimize(self.keynotes, info),
        ]


@strawberry.field(permission_classes=[CanEditSchedule])
def search_events_for_schedule(
    info: Info, conference_id: strawberry.ID, query: str
) -> SearchEventsForScheduleResult:
    proposals = (
        SubmissionModel.objects.for_conference(conference_id)
        .filter(
            Q(status=SubmissionModel.STATUS.accepted)
            | Q(pending_status=SubmissionModel.STATUS.accepted)
        )
        .filter(
            Q(title__icontains=query)
            | Q(speaker__full_name__icontains=query)
            | Q(speaker__name__icontains=query)
        )
        .all()[:5]
    )
    keynotes = (
        KeynoteModel.objects.for_conference(conference_id)
        .filter(Q(title__icontains=query) | Q(speakers__name__icontains=query))
        .all()
    )

    return SearchEventsForScheduleResult(
        conference_id=int(conference_id),
        proposals=proposals,
        keynotes=keynotes,
    )
