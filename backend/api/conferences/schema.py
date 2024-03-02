from api.context import Info
import strawberry

from conferences.models import Conference

from . import types


@strawberry.type
class ConferenceQuery:
    @strawberry.field
    def conference(self, info: Info, code: str) -> types.Conference:
        return Conference.objects.prefetch_related("durations").get(code=code)
