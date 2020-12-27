from decimal import Decimal

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
