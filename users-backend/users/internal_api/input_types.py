import strawberry


@strawberry.input
class LoginInput:
    email: str
    password: str
    staff_only: bool
