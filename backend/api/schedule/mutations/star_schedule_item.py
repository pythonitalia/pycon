from api.context import Info
from api.permissions import IsAuthenticated
from api.users.types import OperationSuccess
from schedule.models import ScheduleItemStar
import strawberry


@strawberry.field(permission_classes=[IsAuthenticated])
def star_schedule_item(info: Info, id: strawberry.ID) -> OperationSuccess:
    user_id = info.context.request.user.id

    ScheduleItemStar.objects.update_or_create(
        user_id=user_id,
        schedule_item_id=id,
    )
    return OperationSuccess(ok=True)
