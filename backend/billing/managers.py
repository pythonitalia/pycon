from conferences.querysets import ConferenceQuerySetMixin


class BillingAddressQuerySet(ConferenceQuerySetMixin):
    def of_user(self, user):
        return self.filter(user=user)
