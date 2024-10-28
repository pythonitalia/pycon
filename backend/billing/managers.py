from django.db import models

from conferences.querysets import ConferenceQuerySetMixin


class BillingAddressQuerySet(ConferenceQuerySetMixin, models.QuerySet):
    def of_user(self, user):
        return self.filter(user=user)
