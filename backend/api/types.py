import strawberry


@strawberry.type
class OperationResult:
    ok: bool
