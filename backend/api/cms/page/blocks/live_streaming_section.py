from typing import Self
import strawberry


@strawberry.type
class LiveStreamingSection:
    id: strawberry.ID

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            id=block.id,
        )
