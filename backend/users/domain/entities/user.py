from datetime import date, datetime
from enum import Enum
from dataclasses import dataclass
from typing import NewType, Optional


UserID = NewType("UserID", int)


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    NOT_SAY = "not_say"


@dataclass
class User:
    id: UserID
    username: str
    email: str
    full_name: str
    name: str
    gender: Gender
    date_of_birth: date
    country: str
    open_to_recruiting: bool
    open_to_newsletter: bool
    is_active: bool
    is_staff: bool
    last_login: datetime

    # Hashed password
    password: Optional[str] = None
    new_password: Optional[str] = None

    def set_password(self, password: str):
        self.new_password = password

    @property
    def pk(self) -> UserID:
        return self.id
