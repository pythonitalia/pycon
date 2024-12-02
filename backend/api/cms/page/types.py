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
    def from_model(
        cls, obj: GenericPageModel, *, can_see_page: bool | None = None
    ) -> Self:
        match can_see_page:
            case None:
                # They can see it
                # and there are no restrictions
                # so show the whole page
                body = obj.body
            case True:
                # They can see the whole page
                # so skip the first block that is used to tell users to authenticate or similar
                body = obj.body[1:]
            case False:
                # Only show the first block
                # that is used to tell users to authenticate or similar
                body = [obj.body[0]]

        return cls(
            id=obj.id,
            title=obj.seo_title or obj.title,
            search_description=obj.search_description,
            slug=obj.slug,
            body=[get_block(block.block_type).from_block(block) for block in body],
        )
