from django.http.request import HttpRequest
from api.utils import get_ip
from privacy_policy.models import PrivacyPolicyAcceptanceRecord


def record_privacy_policy_acceptance(
    request: HttpRequest, privacy_policy: str
) -> PrivacyPolicyAcceptanceRecord:
    user = request.user
    ip = get_ip(request)
    user_agent = request.headers.get("HTTP_USER_AGENT", "")

    return PrivacyPolicyAcceptanceRecord.objects.create(
        user=user,
        ip_address=ip,
        user_agent=user_agent,
        privacy_policy=privacy_policy,
    )
