from ..builder import create_mutation_type
from .customer_portal import customer_portal
from .do_checkout import do_checkout

Mutation = create_mutation_type("Mutation", [do_checkout, customer_portal])
