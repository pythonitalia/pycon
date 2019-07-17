import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order


@csrf_exempt
def order_webhook(request):
    if request.method != "POST":
        return HttpResponseForbidden()

    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    event = stripe.Webhook.construct_event(request.body, sig_header, webhook_secret)
    payment_intent = event.data.object

    if event.type == "payment_intent.succeeded":
        return handle_payment_success(payment_intent)
    elif event.type == "payment_intent.payment_failed":
        return handle_payment_fail(payment_intent)

    return HttpResponse(status=400)


def handle_payment_success(payment_intent):
    order = Order.objects.get(transaction_id=payment_intent.id)
    order.fullfil()
    order.save()
    return HttpResponse(status=200)


def handle_payment_fail(payment_intent):
    order = Order.objects.get(transaction_id=payment_intent.id)
    order.fail()
    order.save()
    return HttpResponse(status=200)
