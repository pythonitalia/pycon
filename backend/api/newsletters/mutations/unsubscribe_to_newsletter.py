from api.context import Info
import strawberry


@strawberry.mutation
def unsubscribe_to_newsletter(info: Info) -> bool:
    return True
