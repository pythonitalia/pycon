from api.cms.page.types import GenericPage
import strawberry
from django.contrib.contenttypes.models import ContentType
from wagtail_headless_preview.models import PagePreview


@strawberry.field
def page_preview(content_type: str, token: str) -> GenericPage:
    app_label, model = content_type.split(".")

    content_type = ContentType.objects.get(app_label=app_label, model=model)
    page_preview = PagePreview.objects.get(content_type=content_type, token=token)

    page = page_preview.as_page()
    if not page.id:
        page.id = 0

    return GenericPage.from_model(page)
