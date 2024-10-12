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
    community_contribution: str
    been_to_other_events: str
    interested_in_volunteering: InterestedInVolunteering
    needs_funds_for_travel: bool
    need_visa: bool
    need_accommodation: bool
    why: str
    notes: str
    travelling_from: Optional[str]
    applicant_reply_deadline: Optional[datetime]
    website: str
    twitter_handle: str
    github_handle: str
    linkedin_url: str
    mastodon_handle: str

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
            community_contribution=grant.community_contribution,
            been_to_other_events=grant.been_to_other_events,
            interested_in_volunteering=InterestedInVolunteering(
                grant.interested_in_volunteering
            ),
            needs_funds_for_travel=grant.needs_funds_for_travel,
            need_visa=grant.need_visa,
            need_accommodation=grant.need_accommodation,
            why=grant.why,
            notes=grant.notes,
            travelling_from=grant.travelling_from,
            applicant_reply_deadline=grant.applicant_reply_deadline,
            website=grant.website,
            twitter_handle=grant.twitter_handle,
            github_handle=grant.github_handle,
            linkedin_url=grant.linkedin_url,
            mastodon_handle=grant.mastodon_handle,
        )
