import strawberry

from conferences.models import Conference
from strawberry.types import Info

from . import types


@strawberry.type
class ConferenceQuery:
    @strawberry.field
    async def conference(self, info: Info, code: str) -> types.Conference:
        return await Conference.objects.prefetch_related("durations").aget(code=code)
