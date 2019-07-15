from payments.providers.provider import PaymentProvider


def test_provider_interface():
    class TestProvider(PaymentProvider):
        def charge(self, *, order, payload):
            return super().charge(order=order, payload=payload)

        def setup(cls):
            return super().setup()

    base_interface = TestProvider()
    base_interface.setup()
    base_interface.charge(order=None, payload=None)
