import strawberry
import strawberry_django

from job_board.models import JobListing

from .types import JobListing as JobListingType


@strawberry.type
class JobBoardQuery:
    @strawberry_django.field
    def job_listings(self, conference: str) -> list[JobListingType]:
        return JobListing.objects.filter(conference__code=conference).order_by("order")

    @strawberry_django.field
    def job_listing(self, slug: str) -> JobListingType | None:
        return JobListing.objects.by_slug(slug).first()
