from __future__ import annotations


import strawberry


@strawberry.type
class OperationSuccess:
    ok: bool
