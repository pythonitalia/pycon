from django_admin_api.schedule.types.user import User
import strawberry


@strawberry.type
class ProposalType:
    id: strawberry.ID
    name: str

    @classmethod
    def from_model(cls, proposal_type):
        return cls(
            id=proposal_type.id,
            name=proposal_type.name,
        )


@strawberry.type
class Language:
    id: strawberry.ID
    name: str
    code: str

    @classmethod
    def from_model(cls, language):
        return cls(
            id=language.id,
            name=language.name,
            code=language.code,
        )


@strawberry.type
class Proposal:
    id: strawberry.ID
    title: str
    duration: int
    type: ProposalType
    languages: list[Language]
    speaker: User

    @classmethod
    def from_model(cls, proposal):
        return cls(
            id=proposal.id,
            title=proposal.title,
            duration=proposal.duration.duration,
            languages=[
                Language.from_model(language) for language in proposal.languages.all()
            ],
            type=ProposalType.from_model(proposal.type),
            speaker=User.from_model(proposal.speaker),
        )
