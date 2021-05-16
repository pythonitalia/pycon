from dataclasses import dataclass
from typing import Any

from django.http.request import HttpRequest
from django.utils.functional import cached_property


@dataclass
class Context:
    request: HttpRequest
    response: Any


@dataclass
class Info:
    context: Context
