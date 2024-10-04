from api.utils import get_ip
import requests
import logging
from privacy_policy.record import record_privacy_policy_acceptance
from conferences.models.conference import Conference
from integrations.flodesk import SubscriptionResult, subscribe
from typing import Annotated, Union
from api.context import Info
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import strawberry
from api.types import BaseErrorType
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
        conference_code: list[str] = strawberry.field(default_factory=list)
        non_field_errors: list[str] = strawberry.field(default_factory=list)

    errors: _SubscribeToNewsletterErrors = None


@strawberry.input
class SubscribeToNewsletterInput:
    email: str
    conference_code: str

    def validate(self) -> SubscribeToNewsletterErrors:
        errors = SubscribeToNewsletterErrors()

        if not self.email:
            errors.add_error("email", "Invalid email address")
        else:
            try:
                validate_email(self.email)
            except ValidationError:
                errors.add_error("email", "Invalid email address")

        if not Conference.objects.filter(code=self.conference_code).exists():
            errors.add_error("conference_code", "Invalid conference code")

        return errors.if_has_errors


SubscribeToNewsletterOutput = Annotated[
    Union[NewsletterSubscribeResult, SubscribeToNewsletterErrors],
    strawberry.union(name="SubscribeToNewsletterOutput"),
]


@strawberry.mutation
def subscribe_to_newsletter(
    info: Info, input: SubscribeToNewsletterInput
) -> SubscribeToNewsletterOutput:
    if errors := input.validate():
        return errors

    conference = Conference.objects.get(code=input.conference_code)
    email = input.email
    request = info.context.request

    try:
        result = NewsletterSubscribeResult(status=subscribe(email, ip=get_ip(request)))
        record_privacy_policy_acceptance(info.context.request, conference, "newsletter")
        return result
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
