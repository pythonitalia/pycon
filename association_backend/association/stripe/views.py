from typing import cast

import stripe
from association.api.mutation.retrieve_checkout_session import UserData
from association.db import get_engine, get_session
from association.domain import services
from association.domain.exceptions import AlreadySubscribed
from association.domain.repositories import AssociationRepository
from association.settings import (
    DOMAIN_URL,
    STRIPE_SUBSCRIPTION_API_KEY,
    STRIPE_SUBSCRIPTION_PRICE_ID,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

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
    async def post(self, request):
        data = await request.json()
        # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
        # Typically this is stored alongside the authenticated user in your database.
        checkout_session_id = data["sessionId"]
        checkout_session = await stripe.checkout.Session.retrieve(checkout_session_id)

        session = await stripe.billing_portal.Session.create(
            customer=checkout_session.customer, return_url=DOMAIN_URL
        )
        return JSONResponse({"url": session.url})


class CreateCheckoutSessionView(HTTPEndpoint):
    def _get_association_repository(self, request):
        return AssociationRepository(
            session=cast(AsyncSession, get_session(get_engine(echo=False)))
        )

    async def post(self, request):

        user_data = UserData(email="fake.user@pycon.it", user_id="12345")

        try:
            subscription = await services.do_checkout(
                user_data,
                association_repository=self._get_association_repository(request),
            )
        except AlreadySubscribed as exc:
            return JSONResponse(
                {
                    "error": {
                        "message": f"You are already subscribed until {exc.expiration_date.isoformat()}"
                    }
                },
                status_code=400,
            )
        else:
            return JSONResponse({"sessionId": subscription.stripe_session_id})
