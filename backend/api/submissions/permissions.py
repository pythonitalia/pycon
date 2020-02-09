from strawberry.permission import BasePermission
from submissions.models import Submission


class CanSeeSubmissionDetail(BasePermission):
    message = "You can't see details for this submission"

    def has_permission(self, source, info):
        user = info.context["request"].user

        conference = source.conference

        if conference.is_voting_closed:
            return True

        if not user.is_authenticated:
            return False

        if user.is_staff or source.speaker == user:
            return True

        if user.has_sent_submission(conference):
            return True

        return user.has_conference_ticket(conference)


class CanSeeSubmissionPrivateFields(BasePermission):
    message = "You can't see the private fields for this submission"

    def has_permission(self, source, info):
        user = info.context["request"].user

        if not user.is_authenticated:
            return False

        return user.is_staff or source.speaker == user


class CanSendComment(BasePermission):
    message = "You can't send a comment"

    def has_permission(self, source, info):
        user = info.context["request"].user

        if user.is_staff:
            return True

        input = info.context["input"]
        submission = Submission.objects.get_by_hashid(input.submission)

        if submission.speaker == user:
            return True

        if user.has_sent_submission(submission.conference):
            return True

        return user.has_conference_ticket(submission.conference)
