import json

from stripe import util

CUSTOMER_SUBSCRIPTION_DELETED_PAYLOAD = util.convert_to_stripe_object(
    json.loads(
        """{
  "api_version": "2019-03-14",
  "created": 1618749605,
  "data": {
    "object": {
      "application_fee_percent": null,
      "billing": "charge_automatically",
      "billing_cycle_anchor": 1618749603,
      "billing_thresholds": null,
      "cancel_at": null,
      "cancel_at_period_end": false,
      "canceled_at": 1618749605,
      "collection_method": "charge_automatically",
      "created": 1618749603,
      "current_period_end": 1621341603,
      "current_period_start": 1618749603,
      "customer": "cus_customer_id",
      "days_until_due": null,
      "default_payment_method": null,
      "default_source": null,
      "default_tax_rates": [],
      "discount": null,
      "ended_at": 1618749605,
      "id": "sub_subscription_id",
      "invoice_customer_balance_settings": {
        "consume_applied_balance_on_void": true
      },
      "items": {
        "data": [
          {
            "billing_thresholds": null,
            "created": 1618749603,
            "id": "si_JKEN2wmDLxVT2P",
            "metadata": {},
            "object": "subscription_item",
            "plan": {
              "active": true,
              "aggregate_usage": null,
              "amount": 2000,
              "amount_decimal": "2000",
              "billing_scheme": "per_unit",
              "created": 1618749602,
              "currency": "usd",
              "id": "plan_JKENDGCcAH5Y3i",
              "interval": "month",
              "interval_count": 1,
              "livemode": false,
              "metadata": {},
              "nickname": null,
              "object": "plan",
              "product": "prod_JKENJb1O14doDh",
              "tiers": null,
              "tiers_mode": null,
              "transform_usage": null,
              "trial_period_days": null,
              "usage_type": "licensed"
            },
            "price": {
              "active": true,
              "billing_scheme": "per_unit",
              "created": 1618749602,
              "currency": "usd",
              "id": "plan_JKENDGCcAH5Y3i",
              "livemode": false,
              "lookup_key": null,
              "metadata": {},
              "nickname": null,
              "object": "price",
              "product": "prod_JKENJb1O14doDh",
              "recurring": {
                "aggregate_usage": null,
                "interval": "month",
                "interval_count": 1,
                "trial_period_days": null,
                "usage_type": "licensed"
              },
              "tiers_mode": null,
              "transform_quantity": null,
              "type": "recurring",
              "unit_amount": 2000,
              "unit_amount_decimal": "2000"
            },
            "quantity": 1,
            "subscription": "sub_JKENNEKZIgQz2D",
            "tax_rates": []
          }
        ],
        "has_more": false,
        "object": "list",
        "total_count": 1,
        "url": "/v1/subscription_items?subscription=sub_JKENNEKZIgQz2D"
      },
      "latest_invoice": "in_1IhZuxAQv52awOkHz1ksWsEg",
      "livemode": false,
      "metadata": {},
      "next_pending_invoice_item_invoice": null,
      "object": "subscription",
      "pause_collection": null,
      "pending_invoice_item_interval": null,
      "pending_setup_intent": null,
      "pending_update": null,
      "plan": {
        "active": true,
        "aggregate_usage": null,
        "amount": 2000,
        "amount_decimal": "2000",
        "billing_scheme": "per_unit",
        "created": 1618749602,
        "currency": "usd",
        "id": "plan_JKENDGCcAH5Y3i",
        "interval": "month",
        "interval_count": 1,
        "livemode": false,
        "metadata": {},
        "nickname": null,
        "object": "plan",
        "product": "prod_JKENJb1O14doDh",
        "tiers": null,
        "tiers_mode": null,
        "transform_usage": null,
        "trial_period_days": null,
        "usage_type": "licensed"
      },
      "quantity": 1,
      "schedule": null,
      "start": 1618749603,
      "start_date": 1618749603,
      "status": "canceled",
      "tax_percent": null,
      "transfer_data": null,
      "trial_end": null,
      "trial_start": null
    }
  },
  "id": "evt_1IhZv0AQv52awOkHl12LnaqL",
  "livemode": false,
  "object": "event",
  "pending_webhooks": 2,
  "request": {
    "id": "req_rT9f3W7CEVGGop",
    "idempotency_key": null
  },
  "type": "customer.subscription.deleted"
}"""
    )
)

INVOICE_PAID_PAYLOAD = util.convert_to_stripe_object(
    json.loads(
        """{
  "api_version": "2019-03-14",
  "created": 1618062033,
  "data": {
    "object": {
      "account_country": "GB",
      "account_name": "Testen",
      "account_tax_ids": null,
      "amount_due": 1000,
      "amount_paid": 1000,
      "amount_remaining": 0,
      "application_fee_amount": null,
      "attempt_count": 1,
      "attempted": true,
      "auto_advance": false,
      "billing": "charge_automatically",
      "billing_reason": "subscription_create",
      "charge": "ch_1Ieh36AQv52awOkHAOJGVXb2",
      "collection_method": "charge_automatically",
      "created": 1618062031,
      "currency": "gbp",
      "custom_fields": null,
      "customer": "cus_customer_id",
      "customer_address": null,
      "customer_email": "marcoaciernoemail@gmail.com",
      "customer_name": null,
      "customer_phone": null,
      "customer_shipping": null,
      "customer_tax_exempt": "none",
      "customer_tax_ids": [],
      "default_payment_method": null,
      "default_source": null,
      "default_tax_rates": [],
      "description": null,
      "discount": null,
      "discounts": [],
      "due_date": null,
      "ending_balance": 0,
      "footer": null,
      "hosted_invoice_url": "https://invoice.stripe.com/i/acct_1AEbpzAQv52awOkH/invst_JHFYBOjnsmDH6yxnhbD2jeX09nN1QUC",
      "id": "in_1Ieh35AQv52awOkHrNk0JBjD",
      "invoice_pdf": "https://pay.stripe.com/invoice/acct_1AEbpzAQv52awOkH/invst_JHFYBOjnsmDH6yxnhbD2jeX09nN1QUC/pdf",
      "last_finalization_error": null,
      "lines": {
        "data": [
          {
            "amount": 1000,
            "currency": "gbp",
            "description": "1 \u00d7 Iscrizione Associazione Python Italia (at \u00a310.00 / year)",
            "discount_amounts": [],
            "discountable": true,
            "discounts": [],
            "id": "sli_7a6f818189903e",
            "livemode": false,
            "metadata": {},
            "object": "line_item",
            "period": {
              "end": 1649598031,
              "start": 1618062031
            },
            "plan": {
              "active": true,
              "aggregate_usage": null,
              "amount": 1000,
              "amount_decimal": "1000",
              "billing_scheme": "per_unit",
              "created": 1612806117,
              "currency": "gbp",
              "id": "price_1IIdkHAQv52awOkHISxsHtG5",
              "interval": "year",
              "interval_count": 1,
              "livemode": false,
              "metadata": {},
              "nickname": null,
              "object": "plan",
              "product": "prod_IuSf6H0sVxclQQ",
              "tiers": null,
              "tiers_mode": null,
              "transform_usage": null,
              "trial_period_days": null,
              "usage_type": "licensed"
            },
            "price": {
              "active": true,
              "billing_scheme": "per_unit",
              "created": 1612806117,
              "currency": "gbp",
              "id": "price_1IIdkHAQv52awOkHISxsHtG5",
              "livemode": false,
              "lookup_key": null,
              "metadata": {},
              "nickname": null,
              "object": "price",
              "product": "prod_IuSf6H0sVxclQQ",
              "recurring": {
                "aggregate_usage": null,
                "interval": "year",
                "interval_count": 1,
                "trial_period_days": null,
                "usage_type": "licensed"
              },
              "tiers_mode": null,
              "transform_quantity": null,
              "type": "recurring",
              "unit_amount": 1000,
              "unit_amount_decimal": "1000"
            },
            "proration": false,
            "quantity": 1,
            "subscription": "sub_subscription_id",
            "subscription_item": "si_JHFYTzY7HHw2TL",
            "tax_amounts": [],
            "tax_rates": [],
            "type": "subscription",
            "unique_id": "il_1Ieh35AQv52awOkHlHKcmvE7"
          }
        ],
        "has_more": false,
        "object": "list",
        "total_count": 1,
        "url": "/v1/invoices/in_1Ieh35AQv52awOkHrNk0JBjD/lines"
      },
      "livemode": false,
      "metadata": {},
      "next_payment_attempt": null,
      "number": "F668967A-0008",
      "object": "invoice",
      "on_behalf_of": null,
      "paid": true,
      "payment_intent": "pi_1Ieh35AQv52awOkH1SXRtQJr",
      "payment_settings": {
        "payment_method_options": null,
        "payment_method_types": null
      },
      "period_end": 1618062031,
      "period_start": 1618062031,
      "post_payment_credit_notes_amount": 0,
      "pre_payment_credit_notes_amount": 0,
      "receipt_number": null,
      "starting_balance": 0,
      "statement_descriptor": null,
      "status": "paid",
      "status_transitions": {
        "finalized_at": 1618062031,
        "marked_uncollectible_at": null,
        "paid_at": 1618062032,
        "voided_at": null
      },
      "subscription": "sub_subscription_id",
      "subtotal": 1000,
      "tax": null,
      "tax_percent": null,
      "total": 1000,
      "total_discount_amounts": [],
      "total_tax_amounts": [],
      "transfer_data": null,
      "webhooks_delivered_at": null
    }
  },
  "id": "evt_1Ieh38AQv52awOkHQMSLm5AU",
  "livemode": false,
  "object": "event",
  "pending_webhooks": 2,
  "request": {
    "id": "req_7tZTpsoUXh4rvB",
    "idempotency_key": null
  },
  "type": "invoice.paid"
}"""
    )
)
