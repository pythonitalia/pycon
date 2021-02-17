import json

checkout_session_response_fixture = json.dumps(
    {
        "id": "cs_test_a19t0YDgfcTpF2UEoyk71mtl0x6sn9UtibXXLddi3KXyNSTsY6oH7T92h9",
        "object": "checkout.session",
        "allow_promotion_codes": None,
        "amount_subtotal": 500,
        "amount_total": 500,
        "billing_address_collection": "auto",
        "cancel_url": "https://u5n7k.sse.codesandbox.io//canceled.html",
        "client_reference_id": None,
        "currency": "usd",
        "customer": "cus_IuwRvPMyY0etyP",
        "customer_details": {
            "email": "gaetano.test@mailinator.com",
            "tax_exempt": "none",
            "tax_ids": [],
        },
        "customer_email": None,
        "livemode": False,
        "locale": None,
        "metadata": {},
        "mode": "subscription",
        "payment_intent": None,
        "payment_method_types": ["card"],
        "payment_status": "paid",
        "setup_intent": None,
        "shipping": {
            "address": {
                "city": "Bari",
                "country": "US",
                "line1": "via mia",
                "line2": None,
                "postal_code": "70124",
                "state": "LA",
            },
            "name": "Gaetano Antani",
        },
        "shipping_address_collection": {"allowed_countries": ["US", "CA"]},
        "submit_type": None,
        "subscription": "sub_IuwRXamH1tQOxZ",
        "success_url": "https://u5n7k.sse.codesandbox.io//success.html?session_id={CHECKOUT_SESSION_ID}",
        "total_details": {"amount_discount": 0, "amount_tax": 0},
    }
)
