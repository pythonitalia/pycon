import graphene
from donations.models import Donation


class DonateWithStripeInput(graphene.InputObjectType):
    token = graphene.String(required=True)
    amount = graphene.Float(required=True)
    is_public = graphene.Boolean(required=False)


class DonateWithStripe(graphene.Mutation):
    class Arguments:
        input = DonateWithStripeInput(required=True)

    ok = graphene.Boolean()
    error = graphene.String(required=False)

    def mutate(self, info, input):
        Donation.create_donation_with_stripe(
            input.token,
            info.context.user,
            input.amount,
            True if input.is_public is None else info.is_public
        )

        return DonateWithStripe(ok=True)
