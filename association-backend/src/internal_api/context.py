from __future__ import annotations

from dataclasses import dataclass

from starlette.requests import Request

from src.association_membership.domain.repository import AssociationMembershipRepository


@dataclass
class Info:
    context: Context


@dataclass
class Context:
    request: Request

    @property
    def association_repository(self) -> AssociationMembershipRepository:
        return AssociationMembershipRepository()
