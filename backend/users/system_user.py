from users.models import User


def get_system_user() -> User:
    return User.objects.get_or_create(
        email="system@pycon.it",
        defaults={
            "full_name": "System User",
            "name": "System User",
            "is_active": True,
            "is_staff": False,
        },
    )[0]


def get_system_user_id() -> int:
    return get_system_user().id
