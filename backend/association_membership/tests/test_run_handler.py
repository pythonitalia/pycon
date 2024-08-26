from unittest.mock import patch
from association_membership.handlers import run_handler
from association_membership.exceptions import WebhookError


def test_run_handler_non_existing_service():
    run_handler("unknown", "invoice.paid", {})


def test_run_handler_non_existing_event():
    run_handler("stripe", "unknown", {})


def test_run_handler():
    with patch("association_membership.handlers.get_handler") as mock_get_handler:
        mock_get_handler.return_value = lambda x: None
        run_handler("sns", "bounce", {})


def test_run_handler_raising_known_error():
    with patch("association_membership.handlers.get_handler") as mock_get_handler:
        mock_get_handler().side_effect = WebhookError("Known error")
        run_handler("sns", "bounce", {})
