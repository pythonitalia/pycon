import strawberry
import enum


@strawberry.enum
class Spacing(enum.Enum):
    XL = "xl"
    _3XL = "3xl"
