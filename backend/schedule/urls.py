from django.urls import path
from schedule.views import user_schedule_item_favourites_calendar

urlpatterns = [
    path(
        "user-schedule-favourites-calendar/<int:conference_id>/<str:hash_user_id>",
        user_schedule_item_favourites_calendar,
        name="user-schedule-favourites-calendar",
    ),
]
