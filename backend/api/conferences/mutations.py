from conferences.models.conference import Conference
import strawberry
from api.pretix.types import Voucher
from api.pretix.query import get_voucher

from typing import Optional


@strawberry.type
class ConferencesMutations:
    @strawberry.mutation
    def get_conference_voucher(self, conference: str, code: str) -> Optional[Voucher]:
        conference = Conference.objects.get(code=conference)
        return get_voucher(conference, code)
