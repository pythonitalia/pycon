import strawberry


@strawberry.federation.type(keys=["id"], extend=True)
class User:
    id: strawberry.ID = strawberry.federation.field(external=True)
    is_python_italia_member: bool

    @classmethod
    async def resolve_reference(cls, id: str):
        # customer = await CustomersRepository().get_for_user_id(int(id))
        return cls(
            id=id,
            is_python_italia_member=False,
        )
