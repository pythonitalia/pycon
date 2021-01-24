from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Table, Text
from sqlalchemy.orm import registry

mapper_registry = registry()


@dataclass
class User:
    id: int
    password: str = field(init=False)
    username: str
    email: str
    fullname: str
    name: str
    gender: str
    date_birth: date
    open_to_recruiting: bool
    open_to_newsletter: bool
    country: str
    date_joined: datetime
    is_active: bool
    is_staff: bool


user_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("fullname", String(300), nullable=False),
    Column("password", Text(), nullable=False),
    Column("username", String(100), nullable=False),
    Column("email", String(256), nullable=False),
    Column("name", String(300), nullable=False),
    Column("gender", String(10), nullable=False),
    Column("date_birth", Date(), nullable=False),
    Column("open_to_recruiting", Boolean(), default=False, nullable=False),
    Column("open_to_newsletter", Boolean(), default=False, nullable=False),
    Column("country", String(50), nullable=False),
    Column("date_joined", DateTime(), nullable=False),
    Column("is_active", Boolean(), default=True, nullable=False),
    Column("is_staff", Boolean(), default=False, nullable=False),
)

mapper_registry.map_imperatively(User, user_table)
