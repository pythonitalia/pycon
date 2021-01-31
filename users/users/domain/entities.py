from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Table
from sqlalchemy.orm import registry
from starlette.authentication import BaseUser

from users.auth.tokens import generate_token
from users.starlette_password.hashers import check_password, make_password

mapper_registry = registry()


@dataclass
class User(BaseUser):
    username: str
    email: str
    fullname: str
    name: str
    gender: str
    date_birth: Optional[date]
    open_to_recruiting: bool
    open_to_newsletter: bool
    country: str
    date_joined: datetime
    is_active: bool
    is_staff: bool
    is_superuser: bool

    last_login: Optional[datetime] = None
    id: Optional[int] = None
    hashed_password: Optional[str] = field(default=None, repr=False)
    new_password: Optional[str] = field(default=None, repr=False)

    password: InitVar[Optional[str]] = None

    def __post_init__(self, password):
        if password:
            self.hashed_password = make_password(password)

    def generate_token(self) -> str:
        return generate_token(self)

    def check_password(self, password: str) -> bool:
        return check_password(password, self.hashed_password)

    def set_password(self, raw_password: str):
        """
        The password will be changed when the user is saved
        """
        self.new_password = raw_password

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
    Column("email", String(254), nullable=False),
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
)

mapper_registry.map_imperatively(
    User,
    user_table,
    properties={
        "hashed_password": user_table.c.password,
        "fullname": user_table.c.full_name,
    },
)
