import graphene
from donations.models import Donation

from .mutations import DonateWithStripe

class DonationsMutations():

    donate_with_stripe = DonateWithStripe.Field()
