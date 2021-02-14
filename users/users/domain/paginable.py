from dataclasses import dataclass
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import func, select

from users.settings import DEFAULT_PAGINATION_TO

T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    items: list[T]
    count: int


class Paginable(Generic[T]):
    def __init__(self, session: AsyncSession, entity) -> None:
        super().__init__()
        self.session = session
        self.entity = entity

    async def page(self, after: int = 0, to: int = DEFAULT_PAGINATION_TO) -> Page:
        query_total_count = select(func.count(self.entity.id))
        query_entities = (
            select(self.entity).limit(to - after).offset(after).order_by("id")
        )

        total_count = (await self.session.execute(query_total_count)).scalar()
        entities = (await self.session.execute(query_entities)).scalars()

        return Page(items=entities, count=total_count)
