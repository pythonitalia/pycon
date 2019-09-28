import strawberry

from ..helpers.i18n import make_localized_resolver


@strawberry.type
class FAQ:
    question: str = strawberry.field(resolver=make_localized_resolver("question"))
    answer: str = strawberry.field(resolver=make_localized_resolver("answer"))
