from datetime import datetime
from typing import Optional

import strawberry

from ..helpers.i18n import make_localized_resolver


@strawberry.type
class JobListing:
    id: strawberry.ID
    title: str = strawberry.field(resolver=make_localized_resolver("title"))
    slug: str = strawberry.field(resolver=make_localized_resolver("slug"))
    description: str = strawberry.field(resolver=make_localized_resolver("description"))
    company: str
    company_logo: Optional[str]
    apply_url: Optional[str]

    def __init__(self, id: str, title: str, slug: str, description: str, company: str, company_logo: Optional[str], apply_url: Optional[str]) -> None:
        self.id = id
        self.title = title
        self.slug = slug
        self.description = description
        self.company = company
        self.company_logo = company_logo
        self.apply_url = apply_url
