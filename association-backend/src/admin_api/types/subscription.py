from datetime import datetime

import strawberry
from strawberry import ID

from src.association_membership.domain import entities

SubscriptionStatus = strawberry.enum(
    entities.SubscriptionStatus,
    name="SubscriptionStatus",
)

SubscriptionInvoiceStatus = strawberry.enum(
    entities.InvoiceStatus,
    name="SubscriptionInvoiceStatus",
)


@strawberry.type
class MembershipSubscriptionInvoice:
    id: ID
    start: datetime
    end: datetime
    status: SubscriptionInvoiceStatus

    @classmethod
    def from_domain(cls, invoice: entities.SubscriptionInvoice):
        return cls(
            id=invoice.id,
            start=invoice.period_start,
            end=invoice.period_end,
            status=invoice.status,
        )


@strawberry.type
class MembershipSubscription:
    id: ID
    status: SubscriptionStatus
    invoices: list[MembershipSubscriptionInvoice]

    @classmethod
    def from_domain(cls, entity: entities.Subscription):
        return cls(
            id=entity.id,
            status=entity.status,
            invoices=[
                MembershipSubscriptionInvoice.from_domain(invoice)
                for invoice in entity.invoices
            ],
        )
