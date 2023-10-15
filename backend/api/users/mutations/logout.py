import strawberry
from django.contrib.auth import logout as django_logout

from api.context import Info
from api.users.types import OperationSuccess


@strawberry.mutation
def logout(info: Info) -> OperationSuccess:
    django_logout(info.context.request)
    return OperationSuccess(ok=True)
