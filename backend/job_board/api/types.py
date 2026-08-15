import strawberry
import strawberry_django
from job_board import models

from api.context import Info


@strawberry_django.type(models.JobListing)
class JobListing:
    id: strawberry.auto
    title: strawberry.auto
    slug: strawberry.auto
    description: strawberry.auto
    company: strawberry.auto
    apply_url: strawberry.auto

    @strawberry_django.field(only=["company_logo"])
    def company_logo(self, info: Info) -> str | None:
        if not self.company_logo:
            return None

        return info.context.request.build_absolute_uri(self.company_logo.url)
