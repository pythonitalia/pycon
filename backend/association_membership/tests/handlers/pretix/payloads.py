ORDER_PAID = {
    "notification_id": 4122,
    "organizer": "test-organizer",
    "event": "local-conf-test",
    "code": "9YKZK",
    "action": "pretix.event.order.paid",
}

ORDER_DATA_WITH_MEMBERSHIP = {
    "code": "9YKZK",
    "status": "p",
    "testmode": False,
    "secret": "bozndi9ck9yh6itl",
    "email": "pretix@example.org",
    "phone": None,
    "locale": "en",
    "datetime": "2021-12-16T01:04:28.286984Z",
    "expires": "2021-12-30T23:59:59Z",
    "payment_date": "2021-12-16",
    "payment_provider": "stripe",
    "fees": [],
    "total": "10.00",
    "comment": "",
    "custom_followup_at": None,
    "invoice_address": {
        "last_modified": "2021-12-16T01:04:28.289855Z",
        "is_business": False,
        "company": "",
        "name": "gdfgf",
        "name_parts": {"_scheme": "full", "full_name": "gdfgf"},
        "street": "gdfgdf",
        "zipcode": "gdfgdf",
        "city": "gdfdf",
        "country": "AW",
        "state": "",
        "vat_id": "",
        "vat_id_validated": False,
        "internal_reference": "",
    },
    "positions": [
        {
            "id": 801,
            "order": "9YKZK",
            "positionid": 1,
            "item": 100,
            "variation": None,
            "price": "10.00",
            "attendee_name": None,
            "attendee_name_parts": {},
            "company": None,
            "street": None,
            "zipcode": None,
            "city": None,
            "country": None,
            "state": None,
            "attendee_email": None,
            "voucher": None,
            "tax_rate": "0.00",
            "tax_value": "0.00",
            "secret": "123456",
            "addon_to": None,
            "subevent": None,
            "checkins": [],
            "downloads": [
                {
                    "output": "pdf",
                    "url": "http://tickets.pycon.it/api/v1/organizers/test-organizer/events/local-conf-test/orderpositions/801/download/pdf/",
                }
            ],
            "answers": [],
            "tax_rule": 8,
            "pseudonymization_id": "8YVKQWXWTX",
            "seat": None,
            "canceled": False,
        }
    ],
    "downloads": [
        {
            "output": "pdf",
            "url": "http://tickets.pycon.it/api/v1/organizers/test-organizer/events/local-conf-test/orders/9YKZK/download/pdf/",
        }
    ],
    "checkin_attention": False,
    "last_modified": "2021-12-16T01:04:43.149421Z",
    "payments": [
        {
            "local_id": 1,
            "state": "confirmed",
            "amount": "10.00",
            "created": "2021-12-16T01:04:28.318676Z",
            "payment_date": "2021-12-16T01:04:43.0Z",
            "provider": "stripe",
            "payment_url": None,
            "details": {
                "id": "pi_xxxxxxxxxx",
                "payment_method": "pm_xxxxxxxxxxxxxxxxxx",
            },
        }
    ],
    "refunds": [],
    "require_approval": False,
    "sales_channel": "web",
    "url": "https://tickets.pycon.it/test-organizer/local-conf-test/order/9YKZK/bozndi9ck9yh6itl/",
    "customer": None,
}

ORDER_DATA_WITHOUT_MEMBERSHIP = {
    "code": "9YKZK",
    "status": "p",
    "testmode": False,
    "secret": "bozndi9ck9yh6itl",
    "email": "pretix@example.org",
    "phone": None,
    "locale": "en",
    "datetime": "2021-12-16T01:04:28.286984Z",
    "expires": "2021-12-30T23:59:59Z",
    "payment_date": "2021-12-16",
    "payment_provider": "stripe",
    "fees": [],
    "total": "10.00",
    "comment": "",
    "custom_followup_at": None,
    "invoice_address": {
        "last_modified": "2021-12-16T01:04:28.289855Z",
        "is_business": False,
        "company": "",
        "name": "gdfgf",
        "name_parts": {"_scheme": "full", "full_name": "gdfgf"},
        "street": "gdfgdf",
        "zipcode": "gdfgdf",
        "city": "gdfdf",
        "country": "AW",
        "state": "",
        "vat_id": "",
        "vat_id_validated": False,
        "internal_reference": "",
    },
    "positions": [
        {
            "id": 801,
            "order": "9YKZK",
            "positionid": 1,
            "item": 200,
            "variation": None,
            "price": "10.00",
            "attendee_name": None,
            "attendee_name_parts": {},
            "company": None,
            "street": None,
            "zipcode": None,
            "city": None,
            "country": None,
            "state": None,
            "attendee_email": None,
            "voucher": None,
            "tax_rate": "0.00",
            "tax_value": "0.00",
            "secret": "123456",
            "addon_to": None,
            "subevent": None,
            "checkins": [],
            "downloads": [
                {
                    "output": "pdf",
                    "url": "http://tickets.pycon.it/api/v1/organizers/test-organizer/events/local-conf-test/orderpositions/801/download/pdf/",
                }
            ],
            "answers": [],
            "tax_rule": 8,
            "pseudonymization_id": "8YVKQWXWTX",
            "seat": None,
            "canceled": False,
        }
    ],
    "downloads": [
        {
            "output": "pdf",
            "url": "http://tickets.pycon.it/api/v1/organizers/test-organizer/events/local-conf-test/orders/9YKZK/download/pdf/",
        }
    ],
    "checkin_attention": False,
    "last_modified": "2021-12-16T01:04:43.149421Z",
    "payments": [
        {
            "local_id": 1,
            "state": "confirmed",
            "amount": "10.00",
            "created": "2021-12-16T01:04:28.318676Z",
            "payment_date": "2021-12-16T01:04:43.0Z",
            "provider": "stripe",
            "payment_url": None,
            "details": {
                "id": "pi_xxxxxxxxxx",
                "payment_method": "pm_xxxxxxxxxxxxxxxxxx",
            },
        }
    ],
    "refunds": [],
    "require_approval": False,
    "sales_channel": "web",
    "url": "https://tickets.pycon.it/test-organizer/local-conf-test/order/9YKZK/bozndi9ck9yh6itl/",
    "customer": None,
}

ITEMS_WITH_CATEGORY = {
    "count": 1,
    "next": None,
    "previous": None,
    "results": [
        {
            "id": 100,
            "category": 25,
            "name": {
                "en": "Python Italia Association Membership 2022",
                "it": "Iscrizione all'associazione Python Italia 2022",
            },
            "internal_name": None,
            "active": True,
            "sales_channels": ["web"],
            "description": {},
            "default_price": "10.00",
            "free_price": False,
            "tax_rate": "0.00",
            "tax_rule": 8,
            "admission": False,
            "position": 9,
            "picture": None,
            "available_from": None,
            "available_until": None,
            "require_voucher": False,
            "hide_without_voucher": False,
            "allow_cancel": True,
            "require_bundling": False,
            "min_per_order": None,
            "max_per_order": None,
            "checkin_attention": False,
            "has_variations": False,
            "variations": [],
            "addons": [],
            "bundles": [],
            "original_price": None,
            "require_approval": False,
            "generate_tickets": None,
            "show_quota_left": None,
            "hidden_if_available": None,
            "allow_waitinglist": True,
            "issue_giftcard": False,
            "meta_data": {},
            "require_membership": False,
            "require_membership_types": [],
            "require_membership_hidden": False,
            "grant_membership_type": None,
            "grant_membership_duration_like_event": True,
            "grant_membership_duration_days": 0,
            "grant_membership_duration_months": 0,
        }
    ],
}

CATEGORIES = {
    "count": 5,
    "next": None,
    "previous": None,
    "results": [
        {
            "id": 16,
            "name": {"en": "Tickets"},
            "internal_name": None,
            "description": {},
            "position": 0,
            "is_addon": False,
        },
        {
            "id": 17,
            "name": {"en": "Hotel"},
            "internal_name": None,
            "description": {},
            "position": 0,
            "is_addon": False,
        },
        {
            "id": 18,
            "name": {"en": "Gadget"},
            "internal_name": None,
            "description": {},
            "position": 0,
            "is_addon": False,
        },
        {
            "id": 22,
            "name": {"en": "Tickets Student", "it": "Biglietti Studenti"},
            "internal_name": None,
            "description": {
                "en": "Category Tickets Student",
                "it": "Biglietti Categoria Studenti",
            },
            "position": 0,
            "is_addon": False,
        },
        {
            "id": 25,
            "name": {"en": "Association", "it": "Associazione"},
            "internal_name": "Association",
            "description": {"en": "Association", "it": "Association"},
            "position": 0,
            "is_addon": False,
        },
    ],
}

ORDER_DATA_WITH_REFUNDS = {
    "code": "9YKZK",
    "status": "p",
    "testmode": False,
    "secret": "yp46s8dnh9work02",
    "email": "pretix@example.org",
    "phone": None,
    "locale": "en",
    "datetime": "2021-12-16T01:44:50.846879Z",
    "expires": "2022-01-06T23:59:59Z",
    "payment_date": "2021-12-16",
    "payment_provider": "manual",
    "fees": [],
    "total": "10.00",
    "comment": "",
    "custom_followup_at": None,
    "invoice_address": {
        "last_modified": "2021-12-16T01:44:50.853572Z",
        "is_business": False,
        "company": "",
        "name": "sdfds",
        "name_parts": {"_scheme": "full", "full_name": "sdfds"},
        "street": "sdfdsfsd",
        "zipcode": "ddfds",
        "city": "fsdfds",
        "country": "AW",
        "state": "",
        "vat_id": "",
        "vat_id_validated": False,
        "internal_reference": "",
    },
    "positions": [
        {
            "id": 804,
            "order": "9YKZK",
            "positionid": 1,
            "item": 100,
            "variation": None,
            "price": "10.00",
            "attendee_name": None,
            "attendee_name_parts": {},
            "company": None,
            "street": None,
            "zipcode": None,
            "city": None,
            "country": None,
            "state": None,
            "attendee_email": None,
            "voucher": None,
            "tax_rate": "0.00",
            "tax_value": "0.00",
            "secret": "52wh5vnx5gkrhtcbgu5u3zgx7eyvy52e",
            "addon_to": None,
            "subevent": None,
            "checkins": [],
            "downloads": [
                {
                    "output": "pdf",
                    "url": "http://tickets.pycon.it/api/v1/organizers/test-organizer/events/local-conf-test/orderpositions/804/download/pdf/",
                }
            ],
            "answers": [],
            "tax_rule": 8,
            "pseudonymization_id": "33NQRDXMJ3",
            "seat": None,
            "canceled": False,
        }
    ],
    "downloads": [
        {
            "output": "pdf",
            "url": "http://tickets.pycon.it/api/v1/organizers/test-organizer/events/local-conf-test/orders/9YKZK/download/pdf/",
        }
    ],
    "checkin_attention": False,
    "last_modified": "2021-12-16T00:08:47.970914Z",
    "payments": [
        {
            "local_id": 1,
            "state": "confirmed",
            "amount": "10.00",
            "created": "2021-12-16T00:00:50.882421Z",
            "payment_date": "2021-12-16T00:00:01.056360Z",
            "provider": "stripe",
            "payment_url": None,
            "details": {
                "id": "pi_3K791jD5MZ3GejSO1WPYVcsJ",
                "payment_method": "pm_1K791hD5MZ3GejSO0vsNBBp2",
            },
        },
        {
            "local_id": 2,
            "state": "confirmed",
            "amount": "3.00",
            "created": "2021-12-16T00:00:47.943860Z",
            "payment_date": "2021-12-16T00:00:47.949903Z",
            "provider": "manual",
            "payment_url": None,
            "details": {},
        },
    ],
    "refunds": [
        {
            "local_id": 1,
            "state": "done",
            "source": "admin",
            "amount": "3.00",
            "payment": 1,
            "created": "2021-12-16T00:00:05.076318Z",
            "execution_date": "2021-12-16T00:00:06.585765Z",
            "comment": None,
            "provider": "stripe",
        }
    ],
    "require_approval": False,
    "sales_channel": "web",
    "url": "https://tickets.pycon.it/test-organizer/local-conf-test/order/9YKZK/yp46s8dnh9work02/",
    "customer": None,
}

ORDER_DATA_WITH_REFUND_EVERYTHING_BUT_MEMBERSHIP = {
    "code": "9YKZK",
    "status": "p",
    "testmode": False,
    "secret": "257fg221mfd9hdxd",
    "email": "pretix@example.org",
    "phone": None,
    "locale": "en",
    "datetime": "2021-12-16T00:19:48.747751Z",
    "expires": "2022-01-06T23:59:59Z",
    "payment_date": "2021-12-16",
    "payment_provider": "stripe",
    "fees": [],
    "total": "90.00",
    "comment": "",
    "custom_followup_at": None,
    "invoice_address": {
        "last_modified": "2021-12-16T00:19:48.753369Z",
        "is_business": False,
        "company": "",
        "name": "vfgfs",
        "name_parts": {"_scheme": "full", "full_name": "vfgfs"},
        "street": "gfdgdf",
        "zipcode": "423",
        "city": "vf",
        "country": "AU",
        "state": "",
        "vat_id": "",
        "vat_id_validated": False,
        "internal_reference": "",
    },
    "positions": [
        {
            "id": 818,
            "order": "9YKZK",
            "positionid": 1,
            "item": 100,
            "variation": None,
            "price": "10.00",
            "attendee_name": None,
            "attendee_name_parts": {},
            "company": None,
            "street": None,
            "zipcode": None,
            "city": None,
            "country": None,
            "state": None,
            "attendee_email": None,
            "voucher": None,
            "tax_rate": "0.00",
            "tax_value": "0.00",
            "secret": "ja3jm7qq9seedq2edhnwsjm6trv7a52d",
            "addon_to": None,
            "subevent": None,
            "checkins": [],
            "downloads": [
                {
                    "output": "pdf",
                    "url": "http://tickets.pycon.it/api/v1/organizers/test-organizer/events/local-conf-test/orderpositions/818/download/pdf/",
                }
            ],
            "answers": [],
            "tax_rule": 8,
            "pseudonymization_id": "LNSEYS3M8J",
            "seat": None,
            "canceled": False,
        },
        {
            "id": 819,
            "order": "9YKZK",
            "positionid": 2,
            "item": 67,
            "variation": None,
            "price": "80.00",
            "attendee_name": "vfvdf",
            "attendee_name_parts": {"_legacy": "vfvdf"},
            "company": None,
            "street": None,
            "zipcode": None,
            "city": None,
            "country": None,
            "state": None,
            "attendee_email": "vdfvfdv@vsfs.it",
            "voucher": None,
            "tax_rate": "22.00",
            "tax_value": "14.43",
            "secret": "n2aqpyyfr7eszubwqwvdr87jhzgfr42x",
            "addon_to": None,
            "subevent": None,
            "checkins": [],
            "downloads": [
                {
                    "output": "pdf",
                    "url": "http://tickets.pycon.it/api/v1/organizers/test-organizer/events/local-conf-test/orderpositions/819/download/pdf/",
                }
            ],
            "answers": [
                {
                    "question": 31,
                    "answer": "No preferences",
                    "question_identifier": "URHUPTLM",
                    "options": [16],
                    "option_identifiers": ["TRBQ9KH7"],
                }
            ],
            "tax_rule": 6,
            "pseudonymization_id": "QHQHJMTECQ",
            "seat": None,
            "canceled": False,
        },
    ],
    "downloads": [
        {
            "output": "pdf",
            "url": "http://tickets.pycon.it/api/v1/organizers/test-organizer/events/local-conf-test/orders/9YKZK/download/pdf/",
        }
    ],
    "checkin_attention": False,
    "last_modified": "2021-12-16T00:19:59.404591Z",
    "payments": [
        {
            "local_id": 1,
            "state": "confirmed",
            "amount": "90.00",
            "created": "2021-12-16T00:19:48.813365Z",
            "payment_date": "2021-12-16T00:19:59.385206Z",
            "provider": "stripe",
            "payment_url": None,
            "details": {
                "id": "pi_3K9s9BD5MZ3GejSO0S3T4z5X",
                "payment_method": "pm_1K9s99D5MZ3GejSOpPJztfTj",
            },
        }
    ],
    "refunds": [
        {
            "local_id": 1,
            "state": "done",
            "source": "admin",
            "amount": "80.00",
            "payment": 1,
            "created": "2021-12-16T00:20:39.415758Z",
            "execution_date": "2021-12-16T00:20:40.938300Z",
            "comment": None,
            "provider": "stripe",
        }
    ],
    "require_approval": False,
    "sales_channel": "web",
    "url": "https://tickets.pycon.it/test-organizer/local-conf-test/order/9YKZK/257fg221mfd9hdxd/",
    "customer": None,
}

ORDER_DATA_WITH_REFUND_EVERYTHING_AND_NOT_ENOUGH_TO_COVER_MEMBERSHIP = {
    "code": "9YKZK",
    "status": "p",
    "testmode": False,
    "secret": "257fg221mfd9hdxd",
    "email": "pretix@example.org",
    "phone": None,
    "locale": "en",
    "datetime": "2021-12-16T00:19:48.747751Z",
    "expires": "2022-01-06T23:59:59Z",
    "payment_date": "2021-12-16",
    "payment_provider": "stripe",
    "fees": [],
    "total": "90.00",
    "comment": "",
    "custom_followup_at": None,
    "invoice_address": {
        "last_modified": "2021-12-16T00:19:48.753369Z",
        "is_business": False,
        "company": "",
        "name": "vfgfs",
        "name_parts": {"_scheme": "full", "full_name": "vfgfs"},
        "street": "gfdgdf",
        "zipcode": "423",
        "city": "vf",
        "country": "AU",
        "state": "",
        "vat_id": "",
        "vat_id_validated": False,
        "internal_reference": "",
    },
    "positions": [
        {
            "id": 818,
            "order": "9YKZK",
            "positionid": 1,
            "item": 100,
            "variation": None,
            "price": "10.00",
            "attendee_name": None,
            "attendee_name_parts": {},
            "company": None,
            "street": None,
            "zipcode": None,
            "city": None,
            "country": None,
            "state": None,
            "attendee_email": None,
            "voucher": None,
            "tax_rate": "0.00",
            "tax_value": "0.00",
            "secret": "ja3jm7qq9seedq2edhnwsjm6trv7a52d",
            "addon_to": None,
            "subevent": None,
            "checkins": [],
            "downloads": [
                {
                    "output": "pdf",
                    "url": "http://tickets.pycon.it/api/v1/organizers/test-organizer/events/local-conf-test/orderpositions/818/download/pdf/",
                }
            ],
            "answers": [],
            "tax_rule": 8,
            "pseudonymization_id": "LNSEYS3M8J",
            "seat": None,
            "canceled": False,
        },
        {
            "id": 819,
            "order": "9YKZK",
            "positionid": 2,
            "item": 67,
            "variation": None,
            "price": "80.00",
            "attendee_name": "vfvdf",
            "attendee_name_parts": {"_legacy": "vfvdf"},
            "company": None,
            "street": None,
            "zipcode": None,
            "city": None,
            "country": None,
            "state": None,
            "attendee_email": "vdfvfdv@vsfs.it",
            "voucher": None,
            "tax_rate": "22.00",
            "tax_value": "14.43",
            "secret": "n2aqpyyfr7eszubwqwvdr87jhzgfr42x",
            "addon_to": None,
            "subevent": None,
            "checkins": [],
            "downloads": [
                {
                    "output": "pdf",
                    "url": "http://tickets.pycon.it/api/v1/organizers/test-organizer/events/local-conf-test/orderpositions/819/download/pdf/",
                }
            ],
            "answers": [
                {
                    "question": 31,
                    "answer": "No preferences",
                    "question_identifier": "URHUPTLM",
                    "options": [16],
                    "option_identifiers": ["TRBQ9KH7"],
                }
            ],
            "tax_rule": 6,
            "pseudonymization_id": "QHQHJMTECQ",
            "seat": None,
            "canceled": False,
        },
    ],
    "downloads": [
        {
            "output": "pdf",
            "url": "http://tickets.pycon.it/api/v1/organizers/test-organizer/events/local-conf-test/orders/9YKZK/download/pdf/",
        }
    ],
    "checkin_attention": False,
    "last_modified": "2021-12-16T00:19:59.404591Z",
    "payments": [
        {
            "local_id": 1,
            "state": "confirmed",
            "amount": "90.00",
            "created": "2021-12-16T00:19:48.813365Z",
            "payment_date": "2021-12-16T00:19:59.385206Z",
            "provider": "stripe",
            "payment_url": None,
            "details": {
                "id": "pi_3K9s9BD5MZ3GejSO0S3T4z5X",
                "payment_method": "pm_1K9s99D5MZ3GejSOpPJztfTj",
            },
        }
    ],
    "refunds": [
        {
            "local_id": 1,
            "state": "done",
            "source": "admin",
            "amount": "80.00",
            "payment": 1,
            "created": "2021-12-16T00:20:39.415758Z",
            "execution_date": "2021-12-16T00:20:40.938300Z",
            "comment": None,
            "provider": "stripe",
        },
        {
            "local_id": 2,
            "state": "done",
            "source": "admin",
            "amount": "5.00",
            "payment": 1,
            "created": "2021-12-16T00:26:38.941174Z",
            "execution_date": "2021-12-16T00:26:40.569829Z",
            "comment": None,
            "provider": "stripe",
        },
    ],
    "require_approval": False,
    "sales_channel": "web",
    "url": "https://tickets.pycon.it/test-organizer/local-conf-test/order/9YKZK/257fg221mfd9hdxd/",
    "customer": None,
}
