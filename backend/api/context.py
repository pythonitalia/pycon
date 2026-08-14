from dataclasses import dataclass, field
from typing import Any

from django.http.request import HttpRequest
from strawberry.types import Info as StrawberryInfo

from participants import models as participant_models
from voting.models.vote import Vote


@dataclass
class Context:
    request: HttpRequest
    response: Any
    _user_can_vote: bool | None = None
    _participants_data: (
        dict[int, dict[int, participant_models.Participant | None]] | None
    ) = None
    _schedule_participants_loaded_conferences: set[int] = field(default_factory=set)
    _my_votes: dict[int, Vote] | None = None


type Info = StrawberryInfo[Context, Any]
