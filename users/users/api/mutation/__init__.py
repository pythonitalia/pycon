from users.api.builder import create_mutation_type

from .login import login
from .register import register

Mutation = create_mutation_type("Mutation", [login, register])
