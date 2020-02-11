from typing import TYPE_CHECKING, Optional

import strawberry
from strawberry.types.datetime import DateTime

from ..helpers.i18n import make_localized_resolver
from ..helpers.images import resolve_image
from ..helpers.maps import Map, resolve_map

if TYPE_CHECKING:  # pragma: no cover
    from api.conferences.types import Conference


@strawberry.type
class Event:
    id: strawberry.ID
    conference: "Conference"
    title: str = strawberry.field(resolver=make_localized_resolver("title"))
    slug: str = strawberry.field(resolver=make_localized_resolver("slug"))
    content: str = strawberry.field(resolver=make_localized_resolver("content"))
    map: Optional[Map] = strawberry.field(resolver=resolve_map)
    image: Optional[str] = strawberry.field(resolver=resolve_image)
    location_name: Optional[str]
    start: DateTime
    end: DateTime
