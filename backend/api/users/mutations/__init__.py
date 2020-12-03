from api.helpers.strawberry import create_mutation_type

from .legacy import Login, Register, Logout, Update, RequestPasswordResetMutation
from .reset_password import reset_password


UsersMutations = create_mutation_type(
    "UsersMutations",
    [
        reset_password,
        Login.Mutation,
        Register.Mutation,
        Logout.Mutation,
        Update.Mutation,
        RequestPasswordResetMutation.Mutation,
    ],
)

__all__ = ["reset_password", "UsersMutations"]
