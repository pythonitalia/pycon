from dataclasses import dataclass
from typing import Any, Dict, Optional

from django.http.request import HttpRequest

from voting.models.vote import Vote


@dataclass
class Context:
    request: HttpRequest
    response: Any
    _user_can_vote: Optional[bool] = None
    _my_votes: Optional[Dict[int, Vote]] = None


@dataclass
class Info:
    context: Context
