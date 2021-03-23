from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from datetime import date, datetime, timedelta
from typing import Optional

import jwt
from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Table
from sqlalchemy.orm import registry
from starlette.authentication import BaseUser

from users.settings import SECRET_KEY
from users.starlette_password.hashers import (
    check_password,
    is_password_usable,
    make_password,
)

mapper_registry = registry()

UNUSABLE_PASSWORD = object()


@dataclass
class User(BaseUser):
    email: str
    date_joined: datetime

    username: str = ""
    fullname: str = ""
    name: str = ""
    gender: str = ""
    date_birth: Optional[date] = None
    open_to_recruiting: bool = False
    open_to_newsletter: bool = False
    country: str = ""
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False

    last_login: Optional[datetime] = None
    jwt_auth_id: Optional[int] = 1
    id: Optional[int] = None
    hashed_password: Optional[str] = field(default=None, repr=False)
    new_password: Optional[str] = field(default=None, repr=False)

    password: InitVar[Optional[str]] = None

    _authenticated_user: bool = field(init=False, default=False)

    def __post_init__(self, password):
        if password == UNUSABLE_PASSWORD:
            self.hashed_password = make_password(None)
        elif password:
            self.hashed_password = make_password(password)

    def check_password(self, password: str) -> bool:
        return check_password(password, self.hashed_password)

    def set_password(self, raw_password: str):
        """
        The password will be changed when the user is saved
        """
        self.new_password = raw_password

    def has_usable_password(self) -> bool:
        return is_password_usable(self.hashed_password)

    def get_reset_password_jwt_id(self) -> str:
        return f"reset-password:{self.id}:{self.jwt_auth_id}"

    def create_reset_password_token(self) -> str:
        now = datetime.utcnow()
        return jwt.encode(
            {
                "jti": self.get_reset_password_jwt_id(),
                "user_id": self.id,
                "exp": now + timedelta(hours=1),
                "iat": now,
                "iss": "users",
                "aud": "users/reset-password",
            },
            str(SECRET_KEY),
            algorithm="HS256",
        )

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.fullname or self.name


user_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", Integer(), primary_key=True),
    Column("full_name", String(300), nullable=False),
    Column("password", String(128), nullable=False),
    Column("username", String(100), nullable=True),
    Column("email", String(254), unique=True, nullable=False),
    Column("name", String(300), nullable=False),
    Column("gender", String(10), nullable=False),
    Column("date_birth", Date(), nullable=True),
    Column("open_to_recruiting", Boolean(), default=False, nullable=False),
    Column("open_to_newsletter", Boolean(), default=False, nullable=False),
    Column("country", String(50), nullable=False),
    Column("date_joined", DateTime(timezone=True), nullable=False),
    Column("last_login", DateTime(timezone=True), nullable=True),
    Column("is_active", Boolean(), default=True, nullable=False),
    Column("is_staff", Boolean(), default=False, nullable=False),
    Column("is_superuser", Boolean(), default=False, nullable=False),
    Column(
        "jwt_auth_id",
        Integer(),
        default=1,
        server_default="1",
        nullable=False,
    ),
)

mapper_registry.map_imperatively(
    User,
    user_table,
    properties={
        "hashed_password": user_table.c.password,
        "fullname": user_table.c.full_name,
    },
)
