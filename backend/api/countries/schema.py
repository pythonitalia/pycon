from typing import List

import strawberry

from api.countries.types import Country
from countries import countries


@strawberry.type
class CountryQuery:
    @strawberry.field
    def countries(self, info) -> List[Country]:
        return [Country(code=country.code, name=country.name) for country in countries]

    @strawberry.field
    def country(self, info, code: str = "") -> Country:
        country = countries.get(code=code)
        assert country
        return Country(code=country.code, name=country.name)
