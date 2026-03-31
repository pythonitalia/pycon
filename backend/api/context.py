from dataclasses import dataclass
from typing import Any, Dict, Optional, TypeAlias

from django.http.request import HttpRequest
from strawberry.types import Info as StrawberryInfo

from voting.models.vote import Vote


@dataclass
class Context:
    request: HttpRequest
    response: Any
    _user_can_vote: Optional[bool] = None
    _participants_data: Optional[Any] = None
    _my_votes: Optional[Dict[int, Vote]] = None


Info: TypeAlias = StrawberryInfo[Context, Any]
