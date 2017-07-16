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
