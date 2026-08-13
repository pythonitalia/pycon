from api.context import Info
from api.conferences.types import Conference
import strawberry
import strawberry_django
from strawberry_django.optimizer import OptimizerConfig, optimize

from conferences import models


@strawberry.type
class ConferenceQuery:
    @strawberry_django.field
    def conference(self, info: Info, code: str) -> Conference:
        conferences = models.Conference.objects.filter(code=code).prefetch_related(
            "durations"
        )
        return optimize(
            conferences,
            info,
            config=OptimizerConfig(enable_only=False),
        ).get()
