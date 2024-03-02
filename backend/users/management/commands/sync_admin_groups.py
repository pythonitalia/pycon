from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from grants.models import Grant
from reviews.models import ReviewSession, UserReview
from submissions.models import Submission


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.grants_reviewers()
        self.proposals_reviewers()

        self.stdout.write(self.style.SUCCESS("Successfully synced admin groups"))

    def grants_reviewers(self):
        grants_reviewers, _ = Group.objects.get_or_create(name="Grants: Reviewers")
        grants_reviewers.permissions.clear()
        grants_reviewers.permissions.set(
            [
                self.get_permission("view_grant", Grant),
                self.get_permission("view_reviewsession", ReviewSession),
                self.get_permission("review_reviewsession", ReviewSession),
                self.get_permission("view_userreview", UserReview),
            ]
        )

    def proposals_reviewers(self):
        proposals_reviewers, _ = Group.objects.get_or_create(
            name="Proposals: Reviewers"
        )
        proposals_reviewers.permissions.clear()
        proposals_reviewers.permissions.set(
            [
                self.get_permission("view_submission", Submission),
                self.get_permission("view_reviewsession", ReviewSession),
                self.get_permission("review_reviewsession", ReviewSession),
                self.get_permission("view_userreview", UserReview),
            ]
        )

    def get_permission(self, codename, model):
        return Permission.objects.get(
            codename=codename,
            content_type=ContentType.objects.get_for_model(model),
        )
