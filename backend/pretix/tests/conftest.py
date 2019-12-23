import pytest
from users.tests.fake_pretix import FAKE_PRETIX_ITEMS


@pytest.fixture
def pretix_items():
    return FAKE_PRETIX_ITEMS


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
