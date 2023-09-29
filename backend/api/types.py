import math
from typing import Generic, List, TypeVar

import strawberry


@strawberry.type
class OperationResult:
    ok: bool


class BaseErrorType:
    _has_errors: strawberry.Private[bool] = False

    def add_error(self, field: str, message: str):
        self._has_errors = True
        if not self.errors:
            self.errors = self._error_class()

        existing_errors = getattr(self.errors, field, [])
        existing_errors.append(message)
        setattr(self.errors, field, existing_errors)

    @property
    def has_errors(self) -> bool:
        return self._has_errors

    @classmethod
    def with_error(cls, field: str, message: str):
        instance = cls()
        parent = cls._error_class()
        setattr(parent, field, [message])
        instance.errors = parent
        return instance

    @property
    def if_has_errors(self):
        if self.has_errors:
            return self

        return None


@strawberry.input
class MultiLingualInput:
    en: str = ""
    it: str = ""

    def clean(self, languages: list[str]) -> "MultiLingualInput":
        # A clean multi-lingual input is one
        # where only the allowed languages have a value.
        # This means that we won't store old data the user didn't want to save
        new_input = MultiLingualInput()
        for lang in ("it", "en"):
            if lang in languages:
                value = getattr(self, lang)
                setattr(new_input, lang, value)

        return new_input

    def to_dict(self) -> dict:
        return {"en": self.en, "it": self.it}


ItemType = TypeVar("ItemType")


@strawberry.type
class PageInfo:
    total_pages: int
    total_items: int
    page_size: int


@strawberry.type
class Paginated(Generic[ItemType]):
    page_info: PageInfo
    items: List[ItemType]

    @classmethod
    def paginate_list(
        cls, *, items: List[ItemType], page_size: int, total_items: int, page: int
    ) -> "Paginated[ItemType]":
        return Paginated(
            page_info=PageInfo(
                total_pages=math.ceil(total_items / page_size),
                page_size=page_size,
                total_items=total_items,
            ),
            items=items,
        )
