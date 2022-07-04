from dataclasses import dataclass
from typing import Any

from django.http.request import HttpRequest


@dataclass
class Context:
    request: HttpRequest
    response: Any


@dataclass
class Info:
    context: Context
