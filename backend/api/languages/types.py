import strawberry
import strawberry_django
from languages import models


@strawberry_django.type(models.Language)
class Language:
    id: strawberry.auto
    code: strawberry.auto
    name: strawberry.auto
