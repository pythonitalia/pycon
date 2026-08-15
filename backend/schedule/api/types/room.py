import strawberry
import strawberry_django
from schedule import models


@strawberry_django.type(models.Room)
class Room:
    id: strawberry.auto
    name: strawberry.auto
    type: str
