import strawberry

from users.domain import entities


@strawberry.type
class User:
    id: strawberry.ID
    email: str
    is_active: bool
    is_staff: bool
    jwt_auth_id: int

    @classmethod
    def from_domain(cls, user: entities.User):
        return User(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            is_staff=user.is_staff,
            jwt_auth_id=user.jwt_auth_id,
        )
