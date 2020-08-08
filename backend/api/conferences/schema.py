from api.pretix.types import Voucher
from typing import Optional
from conferences.models import conference
import strawberry
from conferences.models import Conference
from api.pretix.query import get_voucher

from . import types


@strawberry.type
class ConferenceQuery:
    @strawberry.field
    def conference(self, info, code: str) -> types.Conference:
        return Conference.objects.prefetch_related("durations", "rooms").get(code=code)

    @strawberry.field
    def voucher(self, info, conference: str, code: str) -> Optional[Voucher]:
        conference = Conference.objects.get(code=conference)
        return get_voucher(conference, code)
