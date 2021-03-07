from typing import cast

import stripe
from association.db import get_engine, get_session
from association.domain import services
from association.domain.entities.subscription_entities import UserData
from association.domain.exceptions import AlreadySubscribed
from association.domain.repositories import AssociationRepository
from association.settings import (
    STRIPE_SUBSCRIPTION_API_KEY,
    STRIPE_SUBSCRIPTION_API_SECRET,
    STRIPE_SUBSCRIPTION_PRICE_ID,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="association/stripe/templates")

stripe.api_key = STRIPE_SUBSCRIPTION_API_SECRET  # 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'


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
        return AssociationRepository(
            session=cast(AsyncSession, get_session(get_engine(echo=False)))
        )

    async def post(self, request):
        data = await request.json()
        checkout_session_id = data["sessionId"]
        association_repository = self._get_association_repository(request)
        checkout_session = await association_repository.get_subscription_by_session_id(
            checkout_session_id
        )
        billing_portal_url = await association_repository.retrieve_customer_portal_session_url(
            checkout_session.stripe_customer_id
        )
        # billing_portal_url = await services.customer_portal(
        #     user_data, association_repository=info.context.association_repository
        # )
        return JSONResponse({"url": billing_portal_url})


class CreateCheckoutSessionView(HTTPEndpoint):
    def _get_association_repository(self, request):
        return AssociationRepository(
            session=cast(AsyncSession, get_session(get_engine(echo=False)))
        )

    async def post(self, request):

        user_data = UserData(email="fake.user3@pycon.it", user_id=12346)

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


class CheckoutSessionDetailView(HTTPEndpoint):
    def _get_association_repository(self, request):
        return AssociationRepository(
            session=cast(AsyncSession, get_session(get_engine(echo=False)))
        )

    async def get(self, request):
        # association_repository = self._get_association_repository(request)
        # checkout_session = await association_repository.get_subscription_by_session_id(
        #     request.query_params.get("sessionId")
        # )
        # return JSONResponse({
        #     "customer_id": checkout_session.stripe_customer_id
        # })
        checkout_session = stripe.checkout.Session.retrieve(
            request.query_params.get("sessionId")
        )
        return JSONResponse(checkout_session)
