from ..builder import create_mutation_type
from .retrieve_checkout_session import retrieve_checkout_session

Mutation = create_mutation_type("Mutation", [retrieve_checkout_session])
