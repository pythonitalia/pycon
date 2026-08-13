import strawberry_django
from schedule import models
from strawberry import auto


@strawberry_django.type(models.Room)
class Room:
    id: auto
    name: auto
    type: str
