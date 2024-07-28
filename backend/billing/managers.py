from django.db import models


class BillingAddressQuerySet(models.QuerySet):
    def of_user(self, user):
        return self.filter(user=user)

    def for_conference_code(self, conference):
        return self.filter(organizer__conferences__code=conference)
