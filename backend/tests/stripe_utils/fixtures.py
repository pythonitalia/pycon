import pytest
import stripe

from django.conf import settings


@pytest.fixture(scope='module')
def stripe_customer_id(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    customer = stripe.Customer.create()

    def delete_customer():
        customer.delete()

    request.addfinalizer(delete_customer)

    return customer['id']
