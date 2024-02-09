import strawberry


@strawberry.type
class Submission:
    id: strawberry.ID
    title: str
    duration: int

    @classmethod
    def from_model(cls, submission):
        return cls(
            id=submission.id,
            title=submission.title,
            duration=submission.duration.duration,
        )
