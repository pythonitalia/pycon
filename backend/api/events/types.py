from datetime import datetime
from typing import Optional

import strawberry

from ..helpers.i18n import make_localized_resolver
from ..helpers.images import resolve_image
from ..helpers.maps import Map, resolve_map
from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from api.conferences.types import Conference


@strawberry.type
class Event:
    id: strawberry.ID
    conference: Annotated["Conference", strawberry.lazy("api.conferences.types")]
    title: str = strawberry.field(resolver=make_localized_resolver("title"))
    slug: str = strawberry.field(resolver=make_localized_resolver("slug"))
    content: str = strawberry.field(resolver=make_localized_resolver("content"))
    map: Optional[Map] = strawberry.field(resolver=resolve_map)
    image: Optional[str] = strawberry.field(resolver=resolve_image)
    location_name: Optional[str]
    start: datetime
    end: datetime
