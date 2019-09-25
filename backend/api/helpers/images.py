from typing import Optional


def resolve_image(root, info) -> Optional[str]:
    if not root.image:
        return None

    return info.context["request"].build_absolute_uri(root.image.url)
