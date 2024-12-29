from enum import Enum
from visa.models import InvitationLetterRequestStatus as InvitationLetterRequestStatusDB
import strawberry


@strawberry.enum
class InvitationLetterOnBehalfOf(Enum):
    SELF = "self"
    OTHER = "other"


@strawberry.enum
class InvitationLetterRequestStatus(Enum):
    PENDING = "pending"
    SENT = "sent"
    REJECTED = "rejected"


def _convert_request_status_to_public(status):
    if status in [
        InvitationLetterRequestStatusDB.PENDING,
        InvitationLetterRequestStatusDB.PROCESSING,
        InvitationLetterRequestStatusDB.PROCESSED,
        InvitationLetterRequestStatusDB.FAILED_TO_GENERATE,
    ]:
        return InvitationLetterRequestStatus.PENDING

    if status == InvitationLetterRequestStatusDB.SENT:
        return InvitationLetterRequestStatus.SENT

    if status == InvitationLetterRequestStatusDB.REJECTED:
        return InvitationLetterRequestStatus.REJECTED


@strawberry.type
class InvitationLetterRequest:
    id: strawberry.ID
    status: InvitationLetterRequestStatus

    @classmethod
    def from_model(cls, instance):
        return cls(
            id=instance.id,
            status=_convert_request_status_to_public(instance.status),
        )


@strawberry.type
class InvitationLetterDocumentPage:
    id: strawberry.ID
    title: str
    content: str

    @classmethod
    def from_object(cls, obj: dict):
        return cls(
            id=obj.get("id"),
            title=obj.get("title"),
            content=obj.get("content"),
        )


@strawberry.type
class InvitationLetterDocumentStructure:
    header: str
    footer: str
    pages: list[InvitationLetterDocumentPage]

    @classmethod
    def from_object(cls, obj: dict):
        return cls(
            header=obj.get("header", ""),
            footer=obj.get("footer", ""),
            pages=[
                InvitationLetterDocumentPage.from_object(page)
                for page in obj.get("pages", [])
            ],
        )


@strawberry.type
class InvitationLetterDocument:
    id: strawberry.ID
    dynamic_document: InvitationLetterDocumentStructure

    @classmethod
    def from_model(cls, instance):
        return cls(
            id=instance.id,
            dynamic_document=InvitationLetterDocumentStructure.from_object(
                instance.dynamic_document or {}
            ),
        )
