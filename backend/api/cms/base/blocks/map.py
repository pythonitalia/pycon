from decimal import Decimal
from typing import Self
from api.cms.page.registry import register_page_block
from api.context import Info
from django.conf import settings
import strawberry


def generate_map_image(
    latitude: Decimal, longitude: Decimal, width: int, height: int, zoom: int
) -> str:
    base = "https://api.mapbox.com/styles/v1/"
    style = "mapbox/streets-v12"
    token = f"access_token={settings.MAPBOX_PUBLIC_API_KEY}"

    coordinates = f"{longitude},{latitude}"
    size = f"{width}x{height}@2x"
    marker = f"pin-s-heart+285A98({coordinates})"

    return f"{base}{style}/static/{marker}/{coordinates},{zoom},0,13/{size}?{token}"


@register_page_block(name="map")
@strawberry.type
class CMSMap:
    id: strawberry.ID
    latitude: Decimal
    longitude: Decimal
    link: str
    zoom: int

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            id=block.id,
            latitude=block.value["latitude"],
            longitude=block.value["longitude"],
            link=block.value["link"],
            zoom=block.value["zoom"],
        )

    @strawberry.field
    def image(
        self,
        info: Info,
        width: int = 1280,
        height: int = 400,
    ) -> str:
        return generate_map_image(
            latitude=self.latitude,
            longitude=self.longitude,
            width=width,
            height=height,
            zoom=self.zoom,
        )
