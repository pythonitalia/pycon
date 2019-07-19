import strawberry

from .models import Conference
from .types import ConferenceType


@strawberry.type
class ConferenceQuery:
    @strawberry.field
    def conference(self, info, code: str) -> ConferenceType:
        return Conference.objects.get(code=code)
