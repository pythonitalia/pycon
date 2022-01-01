from typing import List, Optional

import strawberry

from job_board.models import JobListing

from .types import JobListing as JobListingType


@strawberry.type
class JobBoardQuery:
    @strawberry.field
    def job_listings(self, info) -> List[JobListingType]:
        return [
            JobListingType(
                id=listing.id,
                title=listing.title,
                slug=listing.slug,
                description=listing.description,
                company=listing.company,
                company_logo=(
                    info.context.request.build_absolute_uri(listing.company_logo.url)
                    if listing.company_logo
                    else None
                ),
                apply_url=listing.apply_url,
            )
            for listing in JobListing.objects.all()
        ]

    @strawberry.field
    def job_listing(self, info, slug: str) -> Optional[JobListingType]:
        listing = JobListing.objects.by_slug(slug).first()

        if not listing:
            return None

        return JobListingType(
            id=listing.id,
            title=listing.title,
            slug=listing.slug,
            description=listing.description,
            company=listing.company,
            company_logo=(
                info.context.request.build_absolute_uri(listing.company_logo.url)
                if listing.company_logo
                else None
            ),
            apply_url=listing.apply_url,
        )
