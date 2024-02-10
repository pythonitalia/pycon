from django.db.models import Q
from api.permissions import CanEditSchedule
from api.conferences.types import Keynote
from api.submissions.types import Submission
import strawberry
from submissions.models import Submission as SubmissionModel
from conferences.models import Keynote as KeynoteModel


@strawberry.type
class SearchEventsResult:
    results: list[Submission | Keynote]


@strawberry.field(permission_classes=[CanEditSchedule])
def search_events(conference_id: strawberry.ID, query: str) -> SearchEventsResult:
    proposals = (
        SubmissionModel.objects.for_conference(conference_id)
        .accepted()
        .filter(
            Q(title__icontains=query)
            | Q(speaker__full_name__icontains=query)
            | Q(speaker__name__icontains=query)
        )
        .prefetch_related(
            "duration",
            "type",
            "audience_level",
            "languages",
            "speaker",
        )
        .all()[:5]
    )
    keynotes = KeynoteModel.objects.for_conference(conference_id).filter(
        Q(title__icontains=query) | Q(speakers__name__icontains=query)
    )

    proposals = list(proposals)
    for proposal in proposals:
        proposal.__strawberry_definition__ = Submission.__strawberry_definition__

    return SearchEventsResult(
        results=[
            *proposals,
            *[Keynote.from_django_model(keynote) for keynote in keynotes],
        ]
    )
