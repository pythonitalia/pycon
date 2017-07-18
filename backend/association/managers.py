import datetime

from django.db import models
from users.models import User


class MembershipManager(models.Manager):

    def inactives(self, year=None):
        """Get all user that are not members."""
        if not year:
            date = datetime.datetime.now()
            year = date.year

        members = self.get_queryset().values_list(
            'user', flat=True
        ).filter(
            date__year=year
        )

        return User.objects.filter(
            date_joined__year__lte=year
        ).exclude(pk__in=members)

    def is_member(self, user):
        """Helper to check if user is a member."""
        date = datetime.datetime.now()
        year = date.year

        return self.get_queryset().filter(
            user=user,
            date__year=year
        ).exists()

    def create_membership(self, user):
        """
        Create new mebership.

        TODO: generate with payaments
        """
        return self.create(
            user=user,
        )
