import strawberry


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
