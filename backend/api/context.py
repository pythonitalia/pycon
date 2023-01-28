from dataclasses import dataclass
from typing import Any, Optional

from django.db.models.query import QuerySet
from django.http.request import HttpRequest


@dataclass
class Context:
    request: HttpRequest
    response: Any
    _user_can_vote: Optional[bool] = None
    my_votes: Optional[QuerySet] = None


@dataclass
class Info:
    context: Context
