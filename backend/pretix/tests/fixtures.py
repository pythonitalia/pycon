import pytest


@pytest.fixture
def pretix_questions():
    return {
        "count": 3,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": 1,
                "question": {"en": "Codice Fiscale"},
                "type": "S",
                "required": True,
                "items": [1, 2],
                "options": [],
                "position": 0,
                "ask_during_checkin": False,
                "identifier": "ZZZ",
                "dependency_question": None,
                "dependency_values": [],
                "hidden": False,
                "dependency_value": None,
                "print_on_invoice": False,
            },
            {
                "id": 2,
                "question": {"en": "Food preferences"},
                "type": "C",
                "required": True,
                "items": [1, 2],
                "options": [
                    {
                        "id": 4,
                        "identifier": "AAA",
                        "answer": {"en": "No preferences"},
                        "position": 0,
                    },
                    {
                        "id": 5,
                        "identifier": "BBB",
                        "answer": {"en": "Vegetarian"},
                        "position": 1,
                    },
                    {
                        "id": 6,
                        "identifier": "CCC",
                        "answer": {"en": "Vegan"},
                        "position": 2,
                    },
                ],
                "position": 0,
                "ask_during_checkin": False,
                "identifier": "DDD",
                "dependency_question": None,
                "dependency_values": [],
                "hidden": False,
                "dependency_value": None,
                "print_on_invoice": False,
            },
            {
                "id": 3,
                "question": {"en": "Intollerances / Allergies"},
                "type": "S",
                "required": False,
                "items": [1, 2],
                "options": [],
                "position": 0,
                "ask_during_checkin": False,
                "identifier": "EEE",
                "dependency_question": None,
                "dependency_values": [],
                "hidden": False,
                "dependency_value": None,
                "print_on_invoice": False,
            },
        ],
    }


@pytest.fixture
def pretix_quotas():
    return {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": 1,
                "name": "Ticket Quota",
                "size": 200,
                "available_number": 118,
                "items": [1],
                "variations": [],
                "subevent": None,
                "close_when_sold_out": False,
                "closed": False,
            }
        ],
    }


@pytest.fixture
def pretix_user_tickets():
    return [
        {
            "addon_to": None,
            "answers": [
                {
                    "question": {
                        "id": 2,
                        "question": {"en": "Food preferences", "it": "Cibo"},
                        "type": "C",
                        "required": True,
                        "items": [1, 2],
                        "options": [
                            {
                                "id": 1,
                                "identifier": "9MYPHN7J",
                                "answer": {"en": "Sushi", "it": "Cibo Giapponese"},
                                "position": 0,
                            },
                            {
                                "id": 2,
                                "identifier": "KN98FFNU",
                                "answer": {
                                    "en": "Fiorentina Meat",
                                    "it": "Bistecca Toscana",
                                },
                                "position": 1,
                            },
                            {
                                "id": 3,
                                "identifier": "Q7NEWPZV",
                                "answer": {"en": "Thai", "it": "Thai"},
                                "position": 2,
                            },
                        ],
                        "position": 0,
                        "ask_during_checkin": False,
                        "identifier": "KSXA87CV",
                        "dependency_question": None,
                        "dependency_values": [],
                        "hidden": False,
                        "dependency_value": None,
                        "print_on_invoice": False,
                        "help_text": {},
                        "valid_number_min": None,
                        "valid_number_max": None,
                        "valid_date_min": None,
                        "valid_date_max": None,
                        "valid_datetime_min": None,
                        "valid_datetime_max": None,
                        "valid_file_portrait": False,
                    },
                    "answer": "Bistecca Toscana",
                    "options": [2],
                },
                {
                    "question": {
                        "id": 4,
                        "question": {"en": "Intollerance", "it": "Allergie"},
                        "type": "S",
                        "required": True,
                        "items": [1, 2],
                        "options": [],
                        "position": 0,
                        "ask_during_checkin": False,
                        "identifier": "AFTWBC3U",
                        "dependency_question": None,
                        "dependency_values": [],
                        "hidden": False,
                        "dependency_value": None,
                        "print_on_invoice": False,
                        "help_text": {},
                        "valid_number_min": None,
                        "valid_number_max": None,
                        "valid_date_min": None,
                        "valid_date_max": None,
                        "valid_datetime_min": None,
                        "valid_datetime_max": None,
                        "valid_file_portrait": False,
                    },
                    "answer": "Cat",
                    "options": [],
                },
            ],
            "attendee_email": "sheldon@cooper.com",
            "attendee_name": "Sheldon Cooper",
            "attendee_name_parts": {
                "_scheme": "given_family",
                "given_name": "Sheldon",
                "family_name": "Cooper",
            },
            "canceled": False,
            "city": None,
            "company": None,
            "id": 2,
            "positionid": 2,
            "price": "500.00",
            "pseudonymization_id": "KXZTCRLAHK",
            "secret": "dv2rchu5mj6dw6hsybhr2m38zvrgeqjd",
            "state": None,
            "street": None,
            "subevent": None,
            "tax_rate": "0.00",
            "tax_rule": None,
            "tax_value": "0.00",
            "variation": None,
            "voucher": None,
            "zipcode": None,
            "item": {
                "id": 1,
                "category": 1,
                "name": {"en": "Regular ticket", "it": "Ticket base"},
                "internal_name": None,
                "active": True,
                "sales_channels": ["web"],
                "description": {
                    "en": "Regular ticket fare",
                    "it": "Tariffa biglietto economico",
                },
                "default_price": "500.00",
                "free_price": False,
                "tax_rate": "0.00",
                "tax_rule": None,
                "admission": True,
                "position": 1,
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
                "show_quota_left": True,
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
            },
        }
    ]


@pytest.fixture
def update_user_ticket():
    return {
        "addon_to": None,
        "answers": [
            {
                "answer": "Vegan",
                "option_identifiers": ["AAXXXSSS"],
                "options": [18],
                "question": 31,
                "question_identifier": "AAXXXSSS",
            },
            {
                "answer": "Vegan",
                "option_identifiers": [],
                "options": [],
                "question": 32,
                "question_identifier": "AAXXXSSS",
            },
        ],
        "attendee_email": "sheldon@cooper.com",
        "attendee_name": "Leonard",
        "attendee_name_parts": {"_legacy": "Leonard"},
        "canceled": False,
        "checkins": [],
        "city": None,
        "company": None,
        "country": None,
        "downloads": [
            {
                "output": "pdf",
                "url": "http://tickets.pycon.it/api/v1/organizers/test-organizer/events/local-conf-test/orderpositions/5638/download/pdf/",
            }
        ],
        "id": 5638,
        "item": 67,
        "order": "A3WNA",
        "positionid": 1,
        "price": "80.00",
        "pseudonymization_id": "AAAAZZZZ`",
        "seat": None,
        "secret": "dfafsdfsdfasfasdfaseeee",
        "state": None,
        "street": None,
        "subevent": None,
        "tax_rate": "22.00",
        "tax_rule": 6,
        "tax_value": "14.43",
        "variation": None,
        "voucher": None,
        "zipcode": None,
    }


@pytest.fixture
def pretix_order():
    return {
        "code": "A5AFZ",
        "status": "n",
        "testmode": True,
        "secret": "AAAAAAAAAAAA",
        "email": "user-email@fake.it",
        "locale": "en",
        "datetime": "2019-11-30T17:32:16.692972Z",
        "expires": "2019-12-16T23:59:59Z",
        "payment_date": None,
        "payment_provider": "banktransfer",
        "fees": [],
        "total": "3000.00",
        "comment": "",
        "invoice_address": {
            "last_modified": "2019-11-30T17:32:16.715980Z",
            "is_business": False,
            "company": "",
            "name": "",
            "name_parts": {"_scheme": "full"},
            "street": "",
            "zipcode": "",
            "city": "",
            "country": "",
            "state": "",
            "vat_id": "",
            "vat_id_validated": False,
            "internal_reference": "",
        },
        "positions": [
            {
                "id": 10,
                "order": "U0FPN",
                "positionid": 1,
                "item": 1,
                "variation": None,
                "price": "2000.00",
                "attendee_name": "Jake",
                "attendee_name_parts": {"_scheme": "full", "full_name": "Jake"},
                "attendee_email": None,
                "voucher": None,
                "tax_rate": "0.00",
                "tax_value": "0.00",
                "addon_to": None,
                "secret": "AAAAAA",
                "subevent": None,
                "checkins": [],
                "downloads": [],
                "answers": [
                    {
                        "question": 1,
                        "answer": "2",
                        "question_identifier": "userid",
                        "options": [],
                        "option_identifiers": [],
                    }
                ],
                "tax_rule": None,
                "pseudonymization_id": "AAAAAAAAA",
                "seat": None,
            },
            {
                "id": 11,
                "order": "U0FPN",
                "positionid": 2,
                "item": 2,
                "variation": None,
                "price": "1000.00",
                "attendee_name": "Jack",
                "attendee_name_parts": {"_scheme": "full", "full_name": "Jack"},
                "attendee_email": None,
                "voucher": None,
                "tax_rate": "0.00",
                "tax_value": "0.00",
                "secret": "AAAAAA",
                "addon_to": None,
                "subevent": None,
                "checkins": [],
                "downloads": [],
                "answers": [
                    {
                        "question": 1,
                        "answer": "2",
                        "question_identifier": "userid",
                        "options": [],
                        "option_identifiers": [],
                    }
                ],
                "tax_rule": None,
                "pseudonymization_id": "BBBBBBBB",
                "seat": None,
            },
        ],
        "downloads": [],
        "checkin_attention": False,
        "last_modified": "2019-11-30T17:32:16.739255Z",
        "payments": [
            {
                "local_id": 1,
                "state": "created",
                "amount": "3000.00",
                "created": "2019-11-30T17:32:16.721375Z",
                "payment_date": None,
                "provider": "banktransfer",
                "payment_url": "https://payment-url/",
                "details": {},
            }
        ],
        "refunds": [],
        "require_approval": False,
        "sales_channel": "web",
        "url": "https://fake-order-url/",
    }


@pytest.fixture
def pretix_items():
    return {
        "count": 2,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": 1,
                "category": 1,
                "name": {"en": "Regular ticket", "it": "Ticket base"},
                "internal_name": None,
                "active": True,
                "sales_channels": ["web"],
                "description": {
                    "en": "Regular ticket fare",
                    "it": "Tariffa biglietto economico",
                },
                "default_price": "500.00",
                "free_price": False,
                "tax_rate": "0.00",
                "tax_rule": None,
                "admission": True,
                "position": 0,
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
                "show_quota_left": True,
                "hidden_if_available": None,
                "allow_waitinglist": True,
                "issue_giftcard": False,
            },
            {
                "id": 2,
                "category": 2,
                "name": {"en": "T-shirt"},
                "internal_name": None,
                "active": True,
                "sales_channels": ["web"],
                "description": None,
                "default_price": "1000.00",
                "free_price": False,
                "tax_rate": "0.00",
                "tax_rule": None,
                "admission": True,
                "position": 1,
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
                "variations": [
                    {
                        "active": True,
                        "available_from": None,
                        "available_until": None,
                        "default_price": "20.00",
                        "description": {"en": "slim fit", "it": "Veste poco"},
                        "hide_without_voucher": False,
                        "id": 1,
                        "original_price": None,
                        "position": 0,
                        "price": "25.00",
                        "require_approval": False,
                        "require_membership": False,
                        "require_membership_hidden": False,
                        "require_membership_types": [],
                        "sales_channels": ["web"],
                        "value": {"en": "Small", "it": "Piccola"},
                    },
                    {
                        "active": True,
                        "available_from": None,
                        "available_until": None,
                        "default_price": None,
                        "description": {},
                        "hide_without_voucher": False,
                        "id": 2,
                        "original_price": None,
                        "position": 1,
                        "price": "20.00",
                        "require_approval": False,
                        "require_membership": False,
                        "require_membership_hidden": False,
                        "require_membership_types": [],
                        "sales_channels": ["web"],
                        "value": {"en": "Large", "it": "Grande"},
                    },
                ],
                "addons": [],
                "bundles": [],
                "original_price": None,
                "require_approval": False,
                "generate_tickets": None,
                "show_quota_left": None,
                "hidden_if_available": None,
                "allow_waitinglist": True,
                "issue_giftcard": False,
            },
        ],
    }


@pytest.fixture
def pretix_categories():
    return {
        "count": 3,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": 1,
                "name": {
                    "en": "Tickets",
                    "it": "Biglietti",
                },
                "internal_name": "tickets",
                "description": {"en": ""},
                "position": 0,
                "is_addon": False,
            },
            {
                "id": 2,
                "name": {"en": "Gadget", "it": "Premi"},
                "internal_name": None,
                "description": {"en": "Gadget", "it": "Premi"},
                "position": 0,
                "is_addon": False,
            },
            {
                "id": 3,
                "name": {
                    "en": "Python Italia Association Membership",
                    "it": "Iscrizione all'associazione Python Italia",
                },
                "internal_name": "Association",
                "description": {},
                "position": 0,
                "is_addon": False,
            },
        ],
    }
