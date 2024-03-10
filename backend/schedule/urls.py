from django.urls import path
from schedule.views import schedule_favourites_calendar

urlpatterns = [
    path(
        "ical-schedule-favourites/<int:conference_id>/<str:hash_user_id>",
        schedule_favourites_calendar,
        name="schedule-favourites-calendar",
    ),
]
