from typing import List

from api.context import Info
import strawberry

from api.countries.types import Country
from countries import countries


@strawberry.type
class CountryQuery:
    @strawberry.field
    def countries(self, info: Info) -> List[Country]:
        return [Country(code=country.code, name=country.name) for country in countries]

    @strawberry.field
    def country(self, info: Info, code: str = "") -> Country:
        country = countries.get(code=code)
        if not country:
            raise ValueError(f"'{code}' is not a valid country.")

        return Country(code=country.code, name=country.name)
