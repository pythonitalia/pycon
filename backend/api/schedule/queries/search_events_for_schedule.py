import strawberry
from django.db.models import Q, QuerySet
from strawberry_django.optimizer import OptimizerStore, optimize

from api.conferences.types import Keynote
from api.context import Info
from api.permissions import CanEditSchedule
from api.submissions.types import Submission
from conferences.models import Keynote as KeynoteModel
from submissions.models import Submission as SubmissionModel


@strawberry.type
class SearchEventsForScheduleResult:
    proposals: strawberry.Private[QuerySet[SubmissionModel]]
    keynotes: strawberry.Private[QuerySet[KeynoteModel]]

    @strawberry.field
    def results(self, info: Info) -> list[Submission | Keynote]:
        # The mixed union has to become a list here, so optimize each queryset
        # before Strawberry loses the opportunity to inspect its model type.
        # Keep title explicit because the frontend selects its resolver twice
        # under different aliases.
        proposals = list(
            optimize(
                self.proposals,
                info,
                store=OptimizerStore.with_hints(only=["title", "speaker_id"]),
            )
        )
        keynotes = list(optimize(self.keynotes, info))

        return [*proposals, *keynotes]


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
        proposals=proposals,
        keynotes=keynotes,
    )
