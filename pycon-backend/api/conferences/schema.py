from typing import Optional

import strawberry
from api.pretix.query import get_voucher
from api.pretix.types import Voucher
from conferences.models import Conference, conference

from . import types


@strawberry.type
class ConferenceQuery:
    @strawberry.field
    def conference(self, info, code: str) -> types.Conference:
        return Conference.objects.prefetch_related("durations", "rooms").get(code=code)
