from users import models
from users.domain.entities import User, UserID, Gender


def convert_user(instance: models.User) -> User:
    return User(
        id=UserID(instance.id),
        username=instance.username,
        email=instance.email,
        full_name=instance.full_name,
        name=instance.name,
        gender=Gender(instance.gender),
        date_of_birth=instance.date_birth,
        country=instance.country,
        open_to_recruiting=instance.open_to_recruiting,
        open_to_newsletter=instance.open_to_newsletter,
        is_active=instance.is_active,
        is_staff=instance.is_staff,
        last_login=instance.last_login,
        password=instance.password,
    )
