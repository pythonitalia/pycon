import strawberry


@strawberry.type
class OperationResult:
    ok: bool


class BaseErrorType:
    _has_errors: strawberry.Private[bool] = False

    def add_error(self, field: str, message: str):
        self._has_errors = True

        existing_errors = getattr(self, field, [])
        existing_errors.append(message)
        setattr(self, field, existing_errors)

    @property
    def has_errors(self) -> bool:
        return self._has_errors

    @classmethod
    def with_error(cls, field: str, message: str):
        instance = cls()
        setattr(instance, field, [message])
        return instance


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
