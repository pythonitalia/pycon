from typing import cast

import stripe
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from association.db import get_engine, get_session
from association.domain import services
from association.domain.exceptions import AlreadySubscribed
from association.settings import (
    STRIPE_SECRET_API_KEY,
    STRIPE_SUBSCRIPTION_API_KEY,
    STRIPE_SUBSCRIPTION_PRICE_ID,
    TEST_USER_EMAIL,
    TEST_USER_ID,
)
from association_membership.domain.entities import UserData
from association_membership.domain.repository import AssociationMembershipRepository

templates = Jinja2Templates(directory="association/stripe/templates")


class PaymentView(HTTPEndpoint):
    async def get(self, request):
        return templates.TemplateResponse("index.html", {"request": request})


class PaymentSuccessView(HTTPEndpoint):
    async def get(self, request):
        return templates.TemplateResponse("payment_ok.html", {"request": request})


class PaymentFailView(HTTPEndpoint):
    async def get(self, request):
        return templates.TemplateResponse("payment_fail.html", {"request": request})


class StripeSetupView(HTTPEndpoint):
    def get(self, request):
        return JSONResponse(
            {
                "publishableKey": STRIPE_SUBSCRIPTION_API_KEY,
                "priceId": STRIPE_SUBSCRIPTION_PRICE_ID,
            }
        )


class CustomerPortalView(HTTPEndpoint):
    def _get_association_repository(self, request):
        return AssociationMembershipRepository(
            # session=cast(AsyncSession, get_session(get_engine(echo=False)))
        )

    async def post(self, request):
        # await request.json()
        user_id = TEST_USER_ID
        association_repository = self._get_association_repository(request)
        subscription = await association_repository.get_subscription_by_user_id(user_id)
        billing_portal_url = (
            await association_repository.retrieve_customer_portal_session_url(
                subscription.stripe_customer_id
            )
        )
        return JSONResponse({"url": billing_portal_url})


class CreateCheckoutSessionView(HTTPEndpoint):
    def _get_association_repository(self, request):
        return AssociationMembershipRepository(
            # session=cast(AsyncSession, get_session(get_engine(echo=False)))
        )

    async def post(self, request):

        user_data = UserData(email=TEST_USER_EMAIL, user_id=TEST_USER_ID)

        try:
            checkout_session = await services.subscribe_user_to_association(
                user_data,
                association_repository=self._get_association_repository(request),
            )
            return JSONResponse({"sessionId": checkout_session.id})
        except AlreadySubscribed:
            return JSONResponse(
                {"error": {"message": "You are already subscribed"}},
                status_code=400,
            )


class CheckoutSessionDetailView(HTTPEndpoint):
    def _get_association_repository(self, request):
        return AssociationMembershipRepository(
            # session=cast(AsyncSession, get_session(get_engine(echo=False)))
        )

    async def get(self, request):
        checkout_session = stripe.checkout.Session.retrieve(
            request.query_params.get("sessionId"),
            api_key=STRIPE_SECRET_API_KEY,
        )
        return JSONResponse(checkout_session)
