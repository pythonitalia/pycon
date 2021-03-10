from __future__ import annotations

from typing import Optional

import strawberry


@strawberry.type
class FieldError:
    message: str
    type: str


PydanticError = Optional[list[FieldError]]
