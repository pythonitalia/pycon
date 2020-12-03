from typing import Optional

from users.domain.converters import convert_user
from users.domain.entities import UserID, User
from users import models
from django.contrib.auth.tokens import default_token_generator


class UsersRepository:
    def get_by_id(self, user_id: UserID) -> Optional[User]:
        user = models.User.objects.filter(id=user_id).first()

        if not user:
            return None

        return convert_user(user)

    def validate_reset_password_token(self, user: User, token: str) -> bool:
        return default_token_generator.check_token(user, token)

    def save_user(self, user: User) -> User:
        # TODO: This method should support creating users
        # in the future :)
        db_user = models.User.objects.filter(id=user.id).first()

        if not db_user:
            raise ValueError("Invalid user id")

        if user.new_password:
            db_user.set_password(user.new_password)

        attributes = {
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "name": user.name,
            "gender": user.gender.value,
            "date_of_birth": user.date_of_birth,
            "country": user.country,
            "open_to_recruiting": user.open_to_recruiting,
            "open_to_newsletter": user.open_to_newsletter,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
        }

        for attribute, value in attributes.items():
            setattr(db_user, attribute, value)

        db_user.save()
        return convert_user(db_user)
