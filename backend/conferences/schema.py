import strawberry

from . import types
from .models import Conference


@strawberry.type
class ConferenceQuery:
    @strawberry.field
    def conference(self, info, code: str) -> types.Conference:
        return Conference.objects.get(code=code)
