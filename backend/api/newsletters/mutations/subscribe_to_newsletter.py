import requests
import logging
from integrations.flodesk import SubscriptionResult, subscribe
from typing import Annotated, Union
from api.context import Info
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import strawberry
from api.types import BaseErrorType, OperationResult
from integrations.flodesk import SubscriptionResult as FlodeskSubscriptionResult

logger = logging.getLogger(__name__)


NewsletterMembershipStatus = strawberry.enum(
    FlodeskSubscriptionResult, name="NewsletterSubscriptionResult"
)


@strawberry.type
class NewsletterSubscribeResult:
    status: NewsletterMembershipStatus  # type: ignore


@strawberry.type
class SubscribeToNewsletterErrors(BaseErrorType):
    @strawberry.type
    class _SubscribeToNewsletterErrors:
        email: list[str] = strawberry.field(default_factory=list)

    errors: _SubscribeToNewsletterErrors = None


@strawberry.input
class SubscribeToNewsletterInput:
    email: str

    def validate(self) -> SubscribeToNewsletterErrors:
        errors = SubscribeToNewsletterErrors()

        if not self.email:
            errors.add_error("email", "Email cannot be empty")
        else:
            try:
                validate_email(self.email)
            except ValidationError:
                errors.add_error("email", "Invalid email address")

        return errors.if_has_errors


SubscribeToNewsletterOutput = Annotated[
    Union[OperationResult, SubscribeToNewsletterErrors],
    strawberry.union(name="SubscribeToNewsletterOutput"),
]


@strawberry.mutation
def subscribe_to_newsletter(
    info: Info, input: SubscribeToNewsletterInput
) -> SubscribeToNewsletterErrors:
    if errors := input.validate():
        return errors

    email = input.email
    request = info.context.request

    try:
        return NewsletterSubscribeResult(status=subscribe(email, ip=get_ip(request)))
    except requests.exceptions.HTTPError as e:
        logger.error(
            "Unable to subscribe the user due to flodesk API error %s %s",
            e,
            e.response.text,
            exc_info=True,
        )
    except Exception as e:
        logger.error(
            "Unable to subscribe the user to flodesk due to an error %s",
            e,
            exc_info=True,
        )

    return NewsletterSubscribeResult(status=SubscriptionResult.UNABLE_TO_SUBSCRIBE)


def get_ip(request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        return x_forwarded_for.split(", ")[0]
    return request.META.get("REMOTE_ADDR")
