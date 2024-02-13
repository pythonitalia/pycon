from api.schedule.types.schedule_item import ScheduleItem
from schedule.models import ScheduleItem as ScheduleItemModel
import strawberry
from api.permissions import CanEditSchedule


@strawberry.field(permission_classes=[CanEditSchedule])
def unassigned_schedule_items(conference_id: strawberry.ID) -> list[ScheduleItem]:
    items = ScheduleItemModel.objects.for_conference(conference_id).filter(
        slot__isnull=True
    )
    return items
