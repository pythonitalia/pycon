from api.cms.utils import get_site_by_host
from api.context import Context
import strawberry

from wagtailmenus.models import MainMenu, FlatMenu
from api.cms.menu.types import CMSMenu


@strawberry.field
def cms_menu(
    info: strawberry.Info[Context],
    hostname: str,
    handle: str,
) -> CMSMenu | None:
    site = get_site_by_host(hostname)

    if not site:
        return None

    if handle == "main":
        menu = MainMenu.get_for_site(site)
    else:
        menu = FlatMenu.get_for_site(site=site, handle=handle)

    if not menu:
        return None

    return CMSMenu.from_model(menu)
