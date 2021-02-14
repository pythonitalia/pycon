from typing import Generic, List, Type, TypeVar, cast

import strawberry

from users.domain.paginable import Paginable
from users.settings import DEFAULT_PAGINATION_TO

T = TypeVar("T")


@strawberry.type
class PageInfo:
    count: int
    has_more: bool


@strawberry.type
class Paginated(Generic[T]):
    items: list[T]
    page_info: PageInfo

    @classmethod
    async def paginate(
        cls,
        *,
        paginable: Paginable,
        after: int = 0,
        to: int = DEFAULT_PAGINATION_TO,
        type_class: Type
    ):
        page = await paginable.page(after, to)
        paginated_items = cast(
            List[T], [type_class.from_domain(item) for item in page.items]
        )
        return cls(
            items=paginated_items,
            page_info=PageInfo(
                count=page.count, has_more=after + len(paginated_items) < page.count
            ),
        )
