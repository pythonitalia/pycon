from typing import Optional

import strawberry_django
from job_board.models import JobListing as JobListingModel
from strawberry import auto

from api.context import Info


@strawberry_django.type(JobListingModel)
class JobListing:
    id: auto
    title: auto
    slug: auto
    description: auto
    company: auto
    apply_url: auto

    @strawberry_django.field(only=["company_logo"])
    def company_logo(self, info: Info) -> Optional[str]:
        if not self.company_logo:
            return None

        return info.context.request.build_absolute_uri(self.company_logo.url)
