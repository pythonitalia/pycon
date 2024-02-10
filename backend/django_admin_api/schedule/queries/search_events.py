from django.db.models import Q
from django_admin_api.permissions import CanEditSchedule
from django_admin_api.proposals.types.keynote import Keynote
from django_admin_api.proposals.types.proposal import Proposal
import strawberry
from submissions.models import Submission
from conferences.models import Keynote as KeynoteModel


@strawberry.field(permission_classes=[CanEditSchedule])
def search_events(conference_id: strawberry.ID, query: str) -> list[Proposal | Keynote]:
    proposals = (
        Submission.objects.for_conference(conference_id)
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
    return [
        *[Proposal.from_model(proposal) for proposal in proposals],
        *[Keynote.from_model(keynote) for keynote in keynotes],
    ]
