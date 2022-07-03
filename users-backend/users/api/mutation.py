from strawberry.tools import create_type

from .mutations.login import login
from .mutations.logout import logout
from .mutations.register import register
from .mutations.request_reset_password import request_reset_password
from .mutations.reset_password import reset_password
from .mutations.update_profile import update_profile

Mutation = create_type(
    "Mutation",
    [login, register, request_reset_password, reset_password, update_profile, logout],
)
