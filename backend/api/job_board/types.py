from typing import Optional

import strawberry


@strawberry.type
class JobListing:
    id: strawberry.ID
    title: str
    slug: str
    description: str
    company: str
    company_logo_url: strawberry.Private[Optional[str]]
    apply_url: str

    @strawberry.field
    def company_logo(self, info) -> Optional[str]:
        if not self.company_logo_url:
            return None

        return info.context.request.build_absolute_uri(self.company_logo_url)

    def __init__(
        self,
        id: str,
        title: str,
        slug: str,
        description: str,
        company: str,
        company_logo_url: Optional[str],
        apply_url: str,
    ) -> None:
        self.id = id
        self.title = title
        self.slug = slug
        self.description = description
        self.company = company
        self.company_logo_url = company_logo_url
        self.apply_url = apply_url

    @classmethod
    def from_django_model(cls, instance):
        return cls(
            id=instance.id,
            title=instance.title,
            slug=instance.slug,
            description=instance.description,
            company=instance.company,
            company_logo_url=instance.company_logo.url
            if instance.company_logo
            else None,
            apply_url=instance.apply_url,
        )
