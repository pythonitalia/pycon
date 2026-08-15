from dataclasses import dataclass
from typing import Any

from django.http.request import HttpRequest
from strawberry.types import Info as StrawberryInfo


@dataclass
class Context:
    request: HttpRequest
    response: Any
    _user_can_vote: bool | None = None


type Info = StrawberryInfo[Context, Any]
