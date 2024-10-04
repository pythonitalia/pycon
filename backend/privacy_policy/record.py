from django.http.request import HttpRequest
from api.utils import get_ip
from conferences.models.conference import Conference
from privacy_policy.models import PrivacyPolicyAcceptanceRecord


def record_privacy_policy_acceptance(
    request: HttpRequest,
    conference: Conference,
    privacy_policy: str,
    *,
    email: str = None,
) -> PrivacyPolicyAcceptanceRecord:
    user = request.user
    ip = get_ip(request)
    user_agent = request.headers.get("User-Agent", "")

    return PrivacyPolicyAcceptanceRecord.objects.create(
        user=user if user.is_authenticated else None,
        email=email,
        conference=conference,
        ip_address=ip,
        user_agent=user_agent,
        privacy_policy=privacy_policy,
    )
