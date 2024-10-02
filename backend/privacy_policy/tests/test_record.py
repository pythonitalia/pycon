from conferences.tests.factories import ConferenceFactory
import time_machine
from django.utils import timezone

from privacy_policy.record import record_privacy_policy_acceptance
from users.tests.factories import UserFactory


def test_record_privacy_policy_acceptance(rf):
    conference = ConferenceFactory()

    request = rf.get("/")
    request.user = UserFactory(username="testuser", password="testpassword")
    request.headers = {
        "User-Agent": "Test User Agent",
        "x-forwarded-for": "192.168.0.1",
    }

    accepted_at = timezone.now()

    with time_machine.travel(accepted_at, tick=False):
        record = record_privacy_policy_acceptance(
            request, conference, "test-privacy-policy"
        )

    assert record.user_id == request.user.id
    assert record.accepted_at == accepted_at
    assert record.ip_address == "192.168.0.1"
    assert record.user_agent == "Test User Agent"
    assert record.privacy_policy == "test-privacy-policy"
