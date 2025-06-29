from django.db import models
from submissions.models import Submission
from schedule.models import ScheduleItem
from job_board.models import JobListing
from cms.components.page.tasks import execute_frontend_revalidate
from conferences.models.conference import Conference


def trigger_frontend_revalidate(conference: Conference, object: models.Model):
    if not conference.frontend_revalidate_url:
        return

    for path in get_paths(object):
        for locale in ["en", "it"]:
            execute_frontend_revalidate.delay(
                url=conference.frontend_revalidate_url,
                path=f"/{locale}{path}",
                secret=conference.frontend_revalidate_secret,
            )


def get_paths(object: models.Model) -> list[str]:
    match object:
        case JobListing():
            return [
                f"/jobs/{object.id}",
                "/jobs/",
            ]
        case ScheduleItem(type=ScheduleItem.TYPES.keynote):
            return [
                f"/keynotes/{object.slug}",
            ]
        case ScheduleItem():
            return [
                f"/event/{object.slug}",
            ]
        case Submission(status=Submission.STATUS.accepted):
            schedule_items = ScheduleItem.objects.filter(
                submission_id=object.id,
                conference=object.conference,
            )
            return [f"/event/{schedule_item.slug}" for schedule_item in schedule_items]
        case _:
            return []
