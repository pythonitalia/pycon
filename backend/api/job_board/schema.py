import strawberry

from job_board.models import JobListing

from .types import JobListing as JobListingType


@strawberry.type
class JobBoardQuery:
    @strawberry.field
    def job_listings(self, conference: str) -> list[JobListingType]:
        return [
            JobListingType.from_django_model(listing)
            for listing in JobListing.objects.filter(conference__code=conference).all()
        ]

    @strawberry.field
    def job_listing(self, slug: str) -> JobListingType | None:
        listing = JobListing.objects.by_slug(slug).first()

        if not listing:
            return None

        return JobListingType.from_django_model(listing)
