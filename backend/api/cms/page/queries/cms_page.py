from pretix import user_has_admission_ticket
from api.cms.utils import get_site_by_host
from api.context import Context
from cms.components.page.models import GenericPage as GenericPageModel

import strawberry

from api.cms.page.types import GenericPage, SiteNotFoundError


@strawberry.field
def cms_page(
    info: strawberry.Info[Context],
    hostname: str,
    slug: str,
    language: str,
) -> GenericPage | SiteNotFoundError | None:
    site = get_site_by_host(hostname)

    if not site:
        return SiteNotFoundError(message=f"Site `{hostname}` not found")

    page = GenericPageModel.objects.in_site(site).filter(slug=slug, live=True).first()

    if not page:
        return None

    password_restriction = (
        page.get_view_restrictions().filter(restriction_type="password").first()
    )
    can_see_page = None

    if (
        password_restriction
        and password_restriction.password
        and password_restriction.password.startswith("ticket-")
    ):
        from conferences.models import Conference

        conference_code = password_restriction.password.split("-")[1]
        conference = Conference.objects.get(code=conference_code)

        user = info.context.request.user
        can_see_page = user.is_authenticated and user_has_admission_ticket(
            email=user.email,
            event_organizer=conference.pretix_organizer_id,
            event_slug=conference.pretix_event_id,
        )

    translated_page = (
        page.get_translations(inclusive=True)
        .filter(locale__language_code=language, live=True)
        .first()
    )

    if not translated_page:
        return None

    return GenericPage.from_model(translated_page, can_see_page=can_see_page)
