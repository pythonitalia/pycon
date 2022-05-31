from typing import List

import strawberry

from checklist.models import ChecklistItem as ChecklistItemModel


@strawberry.type
class ChecklistItem:
    id: strawberry.ID
    text: str

    @classmethod
    def from_django(cls, instance):
        return cls(id=instance.id, text=instance.text)


@strawberry.type
class ChecklistQuery:
    @strawberry.field
    def checklist(self) -> List[ChecklistItem]:
        return [
            ChecklistItem.from_django(instance)
            for instance in ChecklistItemModel.objects.all()
        ]
