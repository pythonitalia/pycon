from contextlib import contextmanager
import math
from typing import Generic, List, TypeVar, get_args, get_type_hints

import strawberry


@strawberry.type
class OperationResult:
    ok: bool


class BaseErrorType:
    _has_errors: strawberry.Private[bool] = False

    @contextmanager
    def with_prefix(self, prefix: str):
        self._prefix = prefix
        yield
        del self._prefix

    def add_error(self, field: str, message: str):
        self._has_errors = True

        if not self.errors:
            self.errors = self.__annotations__["errors"]()

        field = f"{self._prefix}.{field}" if hasattr(self, "_prefix") else field
        parts = field.split(".")
        current = self.errors
        list_type = None

        for part in parts[:-1]:
            if isinstance(current, list):
                index = int(part)
                try:
                    current = current[index]
                except IndexError:
                    for _ in range(index - len(current) + 1):
                        current.append(list_type())

                new_instance = list_type()
                current[index] = new_instance
                current = new_instance
                continue

            next_current = getattr(current, part)

            if not isinstance(next_current, list):
                current = next_current
                continue
            else:
                type_hints = get_type_hints(type(current))
                type_hint = type_hints[part]

                list_type = get_args(type_hint)[0]
                current = next_current
                continue

        last_part = parts[-1]

        existing_errors = getattr(current, last_part, [])
        existing_errors.append(message)
        setattr(current, last_part, existing_errors)

    @property
    def has_errors(self) -> bool:
        return self._has_errors

    @classmethod
    def with_error(cls, field: str, message: str):
        instance = cls()
        parent = cls.__annotations__["errors"]()
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
