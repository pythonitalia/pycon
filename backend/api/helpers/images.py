from typing import Optional

from api.context import Info


def resolve_image(root, info: Info) -> Optional[str]:
    if not root.image:
        return None

    return info.context.request.build_absolute_uri(root.image.url)
