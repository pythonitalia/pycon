import strawberry


@strawberry.type
class OperationResult:
    ok: bool


@strawberry.type
class ErrorResult:
    error_message: str
