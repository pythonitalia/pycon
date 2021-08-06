from strawberry.tools import create_type

from .mutations.login import login

Mutation = create_type("Mutation", [login])
