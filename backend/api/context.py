from dataclasses import dataclass

from django.http.request import HttpRequest
from django.utils.functional import cached_property

from users.domain.repository import UsersRepository


@dataclass
class Context:
    request: HttpRequest

    @cached_property
    def users_repository(self) -> UsersRepository:
        return UsersRepository()


@dataclass
class Info:
    context: Context
