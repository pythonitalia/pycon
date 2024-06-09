import strawberry


@strawberry.type
class File:
    id: strawberry.ID
    url: str
    virus: bool | None
    mime_type: str | None

    @classmethod
    def from_django(cls, instance):
        return cls(
            id=str(instance.id),
            url=instance.url,
            virus=instance.virus,
            mime_type=instance.mime_type,
        )
