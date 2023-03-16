from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from countries.constants import CONTINENTS, COUNTRIES

T = TypeVar("T", bound="Base")


class Base(Generic[T]):
    items: List[T]

    def __init__(self):
        self.items = []

    def __getitem__(self, *kwargs):
        return self.items

    def __iter__(self):
        self.index = 0
        return self

    def __len__(self) -> int:
        return len(self.items)

    def __next__(self) -> T:
        if self.index < len(self.items):
            item = self.items[self.index]
            self.index += 1
            return item

        raise StopIteration

    def get(self, **kwargs) -> Optional[T]:
        return next(
            (
                c
                for c in self.items
                if all(getattr(c, k, None) == v for k, v in kwargs.items())
            ),
            None,
        )


@dataclass
class Continent:
    code: str
    name: str

    def __eq__(self, continent: Union[str, Continent]) -> bool:
        if isinstance(continent, str):
            return continent in self.code or continent in self.name
        return continent == self.code


class Continents(Base):
    def __init__(self):
        self.items = [Continent(**continent) for continent in CONTINENTS]


continents = Continents()


@dataclass
class Country:
    code: str
    name: str
    continent: Continent
    emoji: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Country:
        continent = continents.get(code=data["continent"])
        assert continent
        data["continent"] = continent
        return cls(**data)


class Countries(Base):
    def __init__(self):
        self.items = [Country.from_dict(country) for country in COUNTRIES]


countries = Countries()
