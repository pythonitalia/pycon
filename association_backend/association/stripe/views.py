from typing import cast

import pydantic
import stripe
from association.api.mutation.setup_stripe_checkout import UserData
from association.db import get_engine, get_session
from association.domain import services
from association.domain.repositories import AssociationRepository
from association.domain.services import (
    StripeCreateCheckoutInput,
    StripeCustomerInput,
    SubscriptionRequestInput,
)
from association.domain.services.exceptions import StripeCheckoutSessionNotCreated
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
        )  # session=AsyncSession

    async def post(self, request):

        user_data = UserData(email="gaetanodonghia@gmail.com", user_id="12345")

        try:
            customer = await services.get_customer_from_stripe(
                StripeCustomerInput(email=user_data.email)
            )
        except pydantic.ValidationError as e:
            return JSONResponse({"error": {"message": str(e)}}, status_code=400)

        await request.json()
        try:
            checkout_session = await services.create_checkout_session(
                StripeCreateCheckoutInput(
                    customer_email=user_data.email,
                    customer_id=customer.id if customer else "",
                    # price_id=request_data.price_id
                )
            )
            print(f"checkout_session : {checkout_session}")

        except pydantic.ValidationError as e:
            return JSONResponse({"error": {"message": str(e)}}, status_code=400)
        except StripeCheckoutSessionNotCreated as e:
            return JSONResponse({"error": {"message": str(e)}}, status_code=400)

        try:
            input_model = SubscriptionRequestInput(
                session_id=checkout_session.id,
                customer_id=checkout_session.customer_id,
                user_id=user_data.user_id,
            )
            await services.create_subscription_request(
                input_model,
                association_repository=self._get_association_repository(request),
            )
        except pydantic.ValidationError as e:
            return JSONResponse({"error": {"message": str(e)}}, status_code=400)
        else:
            return JSONResponse({"sessionId": checkout_session.id})
