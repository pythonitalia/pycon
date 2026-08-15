from datetime import datetime
from typing import TYPE_CHECKING, Annotated

import strawberry
import strawberry_django

from api.helpers.i18n import make_localized_resolver
from api.helpers.images import resolve_image
from api.helpers.maps import Map, resolve_map
from events import models

if TYPE_CHECKING:
    from api.conferences.types import Conference


@strawberry_django.type(models.Event)
class Event:
    id: strawberry.auto
    conference: Annotated["Conference", strawberry.lazy("api.conferences.types")]
    title: str = strawberry_django.field(
        resolver=make_localized_resolver("title"), only=["title"]
    )
    slug: str = strawberry_django.field(
        resolver=make_localized_resolver("slug"), only=["slug"]
    )
    content: str = strawberry_django.field(
        resolver=make_localized_resolver("content"), only=["content"]
    )
    map: Map | None = strawberry_django.field(
        resolver=resolve_map,
        only=["latitude", "longitude", "map_link"],
    )
    image: str | None = strawberry_django.field(
        resolver=resolve_image,
        only=["image"],
    )
    location_name: str | None = strawberry_django.field(only=["location_name"])
    start: datetime = strawberry_django.field(only=["start"])
    end: datetime = strawberry_django.field(only=["end"])
