from page.models import GenericPage as GenericPageModel
import strawberry
from api.types import GenericPage


@strawberry.type
class Query:
    @strawberry.field
    def page(
        self,
        slug: str,
        locale: str | None = "en",
    ) -> GenericPage | None:
        page = GenericPageModel.objects.filter(
            locale__language_code=locale, slug=slug
        ).first()

        if not page:
            return None

        return GenericPage.from_model(page)


schema = strawberry.Schema(query=Query)
