import strawberry
from conferences.models import Conference

from . import types


@strawberry.type
class ConferenceQuery:
    @strawberry.field
    def conference(self, info, code: str) -> types.Conference:
        return Conference.objects.prefetch_related("durations", "rooms").get(code=code)
