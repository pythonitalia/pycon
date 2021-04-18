from typing import Any

import strawberry
from strawberry.types import Info

from src.api.context import Context


@strawberry.federation.type(extend=True)
class Query:
    @strawberry.field
    async def association_service(self, info: Info[Context, Any]) -> bool:
        return True
