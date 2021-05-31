import strawberry
from pythonit_toolkit.api.permissions import IsStaff


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsStaff])
    def association_backend(self) -> str:
        return "👥"
