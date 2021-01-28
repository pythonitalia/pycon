from users.api.builder import create_mutation_type

from .login import login

Mutation = create_mutation_type("Mutation", [login])
