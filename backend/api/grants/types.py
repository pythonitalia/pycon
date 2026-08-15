import strawberry
import strawberry_django
from strawberry.scalars import JSON

from generic_forms.services import unwrap_answers
from grants import models

Status = strawberry.enum(models.Grant.Status)
AgeGroup = strawberry.enum(models.Grant.AgeGroup)
Occupation = strawberry.enum(models.Grant.Occupation)
GrantType = strawberry.enum(models.Grant.GrantType)


@strawberry_django.type(
    models.Grant,
    only=["status", "pending_status", "country_type"],
)
class Grant:
    id: strawberry.auto
    status: Status
    name: strawberry.auto
    full_name: strawberry.auto

    age_group: AgeGroup | None

    @strawberry_django.field(only=["age_group"])
    def age_group(self) -> AgeGroup | None:
        return AgeGroup(self.age_group) if self.age_group else None

    gender: strawberry.auto
    occupation: Occupation
    grant_type: list[GrantType]
    python_usage: strawberry.auto
    community_contribution: strawberry.auto
    been_to_other_events: strawberry.auto
    needs_funds_for_travel: strawberry.auto
    need_visa: strawberry.auto
    need_accommodation: strawberry.auto
    why: strawberry.auto
    notes: strawberry.auto
    departure_country: strawberry.auto
    nationality: strawberry.auto
    departure_city: strawberry.auto
    applicant_reply_deadline: strawberry.auto

    @strawberry_django.field(
        only=["form_answer_id", "form_answer__answers"],
        select_related=["form_answer"],
    )
    def form_answers(self) -> JSON | None:
        if self.form_answer_id is None:
            return None

        return unwrap_answers(self.form_answer.answers)
