from django_admin_api.schedule.types.schedule_item import ScheduleItem
from schedule.models import ScheduleItem as ScheduleItemModel
import strawberry
from django_admin_api.permissions import CanEditSchedule


@strawberry.field(permission_classes=[CanEditSchedule])
def unassigned_schedule_items(conference_id: strawberry.ID) -> list[ScheduleItem]:
    items = ScheduleItemModel.objects.for_conference(conference_id).filter(
        slot__isnull=True
    )
    return [ScheduleItem.from_model(item) for item in items]
