from __future__ import annotations

import strawberry


@strawberry.mutation
async def logout() -> str:
    return "todo"
