from api.context import Info
from api.conferences.types import Conference
import strawberry

from conferences.models import Conference as ConferenceModel


@strawberry.type
class ConferenceQuery:
    @strawberry.field
    def conference(self, info: Info, code: str) -> Conference:
        return ConferenceModel.objects.prefetch_related("durations").get(code=code)
