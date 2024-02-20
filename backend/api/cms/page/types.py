from typing import Self
from api.cms.page.registry import get_block, get_block_union
from cms.components.page.models import GenericPage as GenericPageModel

import strawberry


@strawberry.type
class SiteNotFoundError:
    message: str


@strawberry.type
class GenericPage:
    id: strawberry.ID
    title: str
    search_description: str
    slug: str
    body: list[get_block_union()]  # type: ignore

    @classmethod
    def from_model(cls, obj: GenericPageModel) -> Self:
        return cls(
            id=obj.id,
            title=obj.seo_title or obj.title,
            search_description=obj.search_description,
            slug=obj.slug,
            body=[get_block(block.block_type).from_block(block) for block in obj.body],
        )
