from decimal import Decimal
from typing import Optional

import strawberry
from django.conf import settings


def generate_map_image(
    latitude: Decimal, longitude: Decimal, width: int, height: int, zoom: int
) -> str:
    base = "https://api.mapbox.com/styles/v1/"
    style = "patrick91/cjz609hxu1em31cp6t3i4wc3z"
    token = f"access_token={settings.MAPBOX_PUBLIC_API_KEY}"

    coordinates = f"{longitude},{latitude}"
    size = f"{width}x{height}@2x"
    marker = f"pin-s-heart+285A98({coordinates})"

    return f"{base}{style}/static/{marker}/{coordinates},{zoom},0,13/{size}?{token}"


@strawberry.type
class Map:
    latitude: Decimal
    longitude: Decimal
    link: Optional[str]

    @strawberry.field
    def image(
        self,
        info,
        width: Optional[int] = 1280,
        height: Optional[int] = 400,
        zoom: Optional[int] = 15,
    ) -> str:
        return generate_map_image(
            latitude=self.latitude,
            longitude=self.longitude,
            width=width,
            height=height,
            zoom=zoom,
        )


def resolve_map(root, info) -> Optional[Map]:
    if not all((root.latitude, root.longitude)):
        return None

    return Map(
        latitude=root.latitude, longitude=root.longitude, link=root.map_link or None
    )
