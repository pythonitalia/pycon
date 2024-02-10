from api.permissions import IsAuthenticated
from schedule.models import ScheduleItemStar
import strawberry
from api.users.types import OperationSuccess


@strawberry.mutation(permission_classes=[IsAuthenticated])
def unstar_schedule_item(info, id: strawberry.ID) -> OperationSuccess:
    user_id = info.context.request.user.id

    ScheduleItemStar.objects.filter(
        user_id=user_id,
        schedule_item_id=id,
    ).delete()
    return OperationSuccess(ok=True)
