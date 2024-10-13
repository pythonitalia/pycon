from django.db import models


class ConferenceQuerySetMixin:
    @property
    def conference_lookup_field(self):
        return getattr(self.model, "conference_reference", "conference")

    def for_conference(self, conference):
        return self.filter(**{self.conference_lookup_field: conference})

    def for_conference_code(self, conference):
        return self.filter(**{f"{self.conference_lookup_field}__code": conference})


class ConferenceVoucherQuerySet(ConferenceQuerySetMixin, models.QuerySet):
    pass
