import uvicorn
from association.api.views import GraphQL
from association.db import get_engine, get_session
from association.settings import DEBUG
from association.stripe import views as stripe_views
from association.webhooks import views as stripe_webhooks
from starlette.applications import Starlette
from starlette.routing import Route

app = Starlette(
    debug=DEBUG,
    routes=[
        Route("/graphql", GraphQL()),
        Route("/payments/stripe/webhook", stripe_webhooks.StripeWebhook),
        # TODO DELETE THESE URLS
        Route(
            "/stripe/create-checkout-session", stripe_views.CreateCheckoutSessionView
        ),
        Route("/stripe/do-payment", stripe_views.PaymentView),
        Route("/stripe/do-payment/success", stripe_views.PaymentSuccessView),
        Route("/stripe/do-payment/fail", stripe_views.PaymentFailView),
        Route("/stripe/setup", stripe_views.StripeSetupView),
        Route("/stripe/customer-portal", stripe_views.CustomerPortalView),
    ],
)


@app.middleware("http")
async def async_session_middleware(request, call_next):
    async with get_session(request.app.state.engine) as session:
        request.state.session = session
        return await call_next(request)


@app.on_event("startup")
async def startup():
    app.state.engine = get_engine()


@app.on_event("shutdown")
async def shutdown():
    await app.state.engine.dispose()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, **{"port": 8001, "host": "0.0.0.0"})
