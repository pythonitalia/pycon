import strawberry

from association.api.context import Info


@strawberry.type
class Query:
    @strawberry.field()
    async def association_service(self, info: Info) -> bool:
        return True
