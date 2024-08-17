from django.core.exceptions import ValidationError
from django.core.validators import validate_email as original_validate_email


def get_ip(request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        return x_forwarded_for.split(", ")[0]
    return request.META.get("REMOTE_ADDR")


def validate_email(email: str) -> bool:
    try:
        original_validate_email(email)
    except ValidationError:
        return False

    return True
