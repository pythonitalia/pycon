import random
from api.context import Info
from api.submissions.permissions import CanSeeSubmissionRestrictedFields

from voting.helpers import check_if_user_can_vote
import strawberry

from api.permissions import CanSeeSubmissions, IsAuthenticated
from api.types import Paginated
from conferences.models import Conference as ConferenceModel
from submissions.models import (
    Submission as SubmissionModel,
    SubmissionTag as SubmissionTagModel,
)
from voting.models.vote import Vote

from .types import Submission, SubmissionTag


@strawberry.type
class SubmissionsQuery:
    @strawberry.field
    def submission(self, info: Info, id: strawberry.ID) -> Submission | None:
        try:
            submission = SubmissionModel.objects.get_by_hashid(id)
        except SubmissionModel.DoesNotExist:
            return None
        except IndexError:
            return None

        if not CanSeeSubmissionRestrictedFields().has_permission(
            source=submission, info=info
        ):
            return None

        return submission

    @strawberry.field()
    def submissions(
        self,
        info: Info,
        code: str,
        languages: list[str] | None = None,
        voted: bool | None = None,
        tags: list[str] | None = None,
        types: list[str] | None = None,
        audience_levels: list[str] | None = None,
        page: int | None = 1,
        page_size: int | None = 50,
        only_accepted: bool = False,
    ) -> Paginated[Submission] | None:
        if page_size > 300:
            raise ValueError("Page size cannot be greater than 300")

        if page_size < 1:
            raise ValueError("Page size must be greater than 0")

        if page < 1:
            raise ValueError("Page must be greater than 0")

        request = info.context.request
        user = request.user
        conference = ConferenceModel.objects.filter(code=code).first()

        if not only_accepted and not IsAuthenticated().has_permission(conference, info):
            raise PermissionError("User not logged in")

        info.context._user_can_vote = (
            check_if_user_can_vote(user, conference) if user.is_authenticated else False
        )

        if not conference or not CanSeeSubmissions().has_permission(
            conference, info, only_accepted=only_accepted
        ):
            raise PermissionError("You need to have a ticket to see submissions")

        qs = conference.submissions.prefetch_related(
            "type",
            "duration",
            "schedule_items",
            "languages",
            "audience_level",
            "tags",
        )

        if only_accepted:
            qs = qs.filter(status=SubmissionModel.STATUS.accepted)
        else:
            qs = qs.filter(status=SubmissionModel.STATUS.proposed)

        if languages:
            qs = qs.filter(languages__code__in=languages)

        if tags:
            qs = qs.filter(tags__id__in=tags)

        if voted:
            qs = qs.filter(votes__user_id=user.id)
        elif voted is not None:
            qs = qs.exclude(id__in=[s.id for s in qs.filter(votes__user_id=user.id)])

        if types:
            qs = qs.filter(type__id__in=types)

        if audience_levels:
            qs = qs.filter(audience_level__id__in=audience_levels)

        qs = qs.order_by("id").distinct()

        all_submissions = list(qs)
        random.Random(user.id).shuffle(all_submissions)

        total_items = len(all_submissions)
        submissions = list(all_submissions[(page - 1) * page_size : page * page_size])

        info.context._my_votes = {
            vote.submission_id: vote
            for vote in Vote.objects.filter(user_id=user.id, submission__in=submissions)
        }

        return Paginated.paginate_list(
            items=submissions,
            page_size=page_size,
            total_items=total_items,
            page=page,
        )

    @strawberry.field
    def submission_tags(self, info: Info) -> list[SubmissionTag]:
        return SubmissionTagModel.objects.order_by("name").all()

    @strawberry.field
    def voting_tags(self, info: Info, conference: str) -> list[SubmissionTag]:
        used_tags = (
            SubmissionModel.objects.filter(
                conference__code=conference,
            )
            .values_list("tags__id", flat=True)
            .distinct()
        )
        return (
            SubmissionTagModel.objects.filter(id__in=used_tags).order_by("name").all()
        )
