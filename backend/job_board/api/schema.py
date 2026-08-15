import strawberry
import strawberry_django

from job_board import models

from .types import JobListing


@strawberry.type
class JobBoardQuery:
    @strawberry_django.field
    def job_listings(self, conference: str) -> list[JobListing]:
        return models.JobListing.objects.filter(conference__code=conference).order_by(
            "order"
        )

    @strawberry_django.field
    def job_listing(self, slug: str) -> JobListing | None:
        return models.JobListing.objects.by_slug(slug).first()
