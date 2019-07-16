from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    name = "payments"

    def ready(self):
        import payments.converter  # noqa

        from payments.providers.stripe import Stripe

        Stripe.setup()
