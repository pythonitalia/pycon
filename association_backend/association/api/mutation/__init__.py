from ..builder import create_mutation_type
from .setup_stripe_checkout import setup_stripe_checkout

Mutation = create_mutation_type("Mutation", [setup_stripe_checkout])
