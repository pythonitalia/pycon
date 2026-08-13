from api.conferences.types import Conference
import strawberry
import strawberry_django

from conferences import models


@strawberry.type
class ConferenceQuery:
    @strawberry_django.field
    def conference(self, code: str) -> Conference:
        return models.Conference.objects.filter(code=code)
