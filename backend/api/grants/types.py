from __future__ import annotations

import strawberry

from grants.models import Grant as GrantModel


@strawberry.type
class Grant:
    id: strawberry.ID
    name: str
    full_name: str
    email: str
    age: int
    gender: str
    occupation: str
    grant_type: str
    python_usage: str
    been_to_other_events: str
    interested_in_volunteering: str
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
            email=grant.email,
            age=grant.age,
            gender=grant.gender,
            occupation=grant.occupation,
            grant_type=grant.grant_type,
            python_usage=grant.python_usage,
            been_to_other_events=grant.been_to_other_events,
            interested_in_volunteering=grant.interested_in_volunteering,
            needs_funds_for_travel=grant.needs_funds_for_travel,
            why=grant.why,
            notes=grant.notes,
            travelling_from=grant.travelling_from,
        )
