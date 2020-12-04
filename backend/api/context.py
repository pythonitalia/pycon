from dataclasses import dataclass

from django.http.request import HttpRequest
from django.utils.functional import cached_property


@dataclass
class Context:
    request: HttpRequest


@dataclass
class Info:
    context: Context
