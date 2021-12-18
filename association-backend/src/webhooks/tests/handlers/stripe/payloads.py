import json

from stripe import util

RAW_INVOICE_PAID_PAYLOAD = json.loads(
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

INVOICE_PAID_PAYLOAD = util.convert_to_stripe_object(RAW_INVOICE_PAID_PAYLOAD)
