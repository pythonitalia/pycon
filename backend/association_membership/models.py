from datetime import datetime
import logging

from django.db import models

from association_membership.enums import PaymentStatus, SubscriptionStatus

logger = logging.getLogger(__name__)


class Subscription(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.PROTECT)
    status: SubscriptionStatus = models.CharField(
        max_length=20,
        choices=SubscriptionStatus.as_choices(),
        default=SubscriptionStatus.PENDING,
        null=False,
    )

    def mark_as_canceled(self):
        self._change_state(SubscriptionStatus.CANCELED)

    def mark_as_active(self):
        self._change_state(SubscriptionStatus.ACTIVE)

    @property
    def is_active(self) -> bool:
        return self.status == SubscriptionStatus.ACTIVE

    def _change_state(self, to: SubscriptionStatus):
        logger.info(
            "Switching subscription_id=%s of user_id=%s"
            " from old_status=%s to status=%s",
            self.id,
            self.user_id,
            self.status,
            to,
        )
        self.status = to

    def add_pretix_payment(
        self,
        *,
        organizer: str,
        event: str,
        order_code: str,
        total: int,
        status: PaymentStatus,
        payment_date: datetime,
        period_start: datetime,
        period_end: datetime,
    ):
        payment = Payment.objects.create(
            idempotency_key=PretixPayment.generate_idempotency_key(
                organizer, event, order_code
            ),
            total=total,
            status=status,
            payment_date=payment_date,
            period_start=period_start,
            period_end=period_end,
            subscription_id=self.id,
        )
        pretix_payment = PretixPayment.objects.create(
            payment=payment,
            order_code=order_code,
            event_organizer=organizer,
            event_id=event,
        )
        return pretix_payment

    def add_stripe_subscription_payment(
        self,
        total: int,
        status: PaymentStatus,
        payment_date: datetime,
        period_start: datetime,
        period_end: datetime,
        stripe_subscription_id: str,
        stripe_invoice_id: str,
        invoice_pdf: str,
    ):
        payment = Payment.objects.create(
            idempotency_key=stripe_invoice_id,
            total=total,
            status=status,
            payment_date=payment_date,
            period_start=period_start,
            period_end=period_end,
            subscription=self.id,
        )
        stripe_subscription_payment = StripeSubscriptionPayment.objects.create(
            payment=payment,
            stripe_subscription_id=stripe_subscription_id,
            stripe_invoice_id=stripe_invoice_id,
            invoice_pdf=invoice_pdf,
        )
        return stripe_subscription_payment


class Payment(models.Model):
    subscription: Subscription = models.ForeignKey(
        Subscription, null=False, on_delete=models.PROTECT
    )
    # idempotency_key is used as a generic method
    # to keep track of "already handled payments"
    # if a payment comes with the
    # same idempotency_key it gets rejected
    idempotency_key: str = models.CharField(max_length=256, null=False, unique=True)
    total: int = models.IntegerField()
    payment_date: datetime = models.DateTimeField()
    period_start: datetime = models.DateTimeField()
    period_end: datetime = models.DateTimeField()
    status: PaymentStatus = models.CharField(
        max_length=20,
        choices=PaymentStatus.as_choices(),
        null=False,
    )

    @staticmethod
    def is_payment_already_processed(idempotency_key: str) -> bool:
        return Payment.objects.filter(idempotency_key=idempotency_key).exists()


class PretixPayment(models.Model):
    payment: Payment = models.ForeignKey(Payment, null=False, on_delete=models.PROTECT)
    order_code: str = models.CharField(max_length=256, unique=True)
    event_organizer: str = models.CharField(max_length=512)
    event_id: str = models.CharField(max_length=512)

    @staticmethod
    def generate_idempotency_key(organizer: str, event: str, order_code: str) -> str:
        return f"{organizer}_{event}_{order_code}"


class StripeSubscriptionPayment(models.Model):
    payment: Payment = models.ForeignKey(Payment, null=False, on_delete=models.PROTECT)
    stripe_subscription_id: str = models.CharField(max_length=256)
    stripe_invoice_id: str = models.CharField(max_length=256, unique=True)
    invoice_pdf: str = models.TextField()


class StripeCustomer(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.PROTECT)
    stripe_customer_id: str = models.CharField(max_length=256, unique=True)
