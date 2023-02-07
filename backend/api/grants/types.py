from __future__ import annotations

from datetime import datetime
from typing import Optional

import strawberry

from grants.models import Grant as GrantModel

Status = strawberry.enum(GrantModel.Status)
AgeGroup = strawberry.enum(GrantModel.AgeGroup)
Occupation = strawberry.enum(GrantModel.Occupation)
GrantType = strawberry.enum(GrantModel.GrantType)
InterestedInVolunteering = strawberry.enum(GrantModel.InterestedInVolunteering)


@strawberry.type
class Grant:
    id: strawberry.ID
    status: Status
    name: str
    full_name: str
    age_group: Optional[AgeGroup]
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
    applicant_reply_deadline: Optional[datetime]
    applicant_message: Optional[str]

    @classmethod
    def from_model(cls, grant: GrantModel) -> Grant:
        return cls(
            id=grant.id,
            status=Status(grant.status),
            name=grant.name,
            full_name=grant.full_name,
            age_group=AgeGroup(grant.age_group) if grant.age_group else None,
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
            applicant_reply_deadline=grant.applicant_reply_deadline,
            applicant_message=grant.applicant_message,
        )
