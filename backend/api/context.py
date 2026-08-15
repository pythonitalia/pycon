from dataclasses import dataclass
from typing import Any

from django.http.request import HttpRequest
from strawberry.types import Info as StrawberryInfo

from voting.models.vote import Vote


@dataclass
class Context:
    request: HttpRequest
    response: Any
    _user_can_vote: bool | None = None
    _my_votes: dict[int, Vote] | None = None


type Info = StrawberryInfo[Context, Any]
