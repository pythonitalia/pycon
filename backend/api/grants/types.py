from __future__ import annotations

import strawberry

from grants.models import Grant as GrantModel

AgeGroup = strawberry.enum(GrantModel.AgeGroup)
Occupation = strawberry.enum(GrantModel.Occupation)
GrantType = strawberry.enum(GrantModel.GrantType)
InterestedInVolunteering = strawberry.enum(GrantModel.InterestedInVolunteering)


@strawberry.type
class Grant:
    id: strawberry.ID
    name: str
    full_name: str
    age_group: AgeGroup
    gender: str
    occupation: Occupation
    grant_type: GrantType
    python_usage: str
    been_to_other_events: str
    interested_in_volunteering: InterestedInVolunteering
    needs_funds_for_travel: bool
    why: str
    notes: str
    travelling_from: str

    @classmethod
    def from_model(cls, grant: GrantModel) -> Grant:
        return cls(
            id=grant.id,
            name=grant.name,
            full_name=grant.full_name,
            age_group=AgeGroup(grant.age_group),
            gender=grant.gender,
            occupation=Occupation(grant.occupation),
            grant_type=GrantType(grant.grant_type),
            python_usage=grant.python_usage,
            been_to_other_events=grant.been_to_other_events,
            interested_in_volunteering=InterestedInVolunteering(
                grant.interested_in_volunteering
            ),
            needs_funds_for_travel=grant.needs_funds_for_travel,
            why=grant.why,
            notes=grant.notes,
            travelling_from=grant.travelling_from,
        )
