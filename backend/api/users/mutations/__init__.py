from strawberry.tools import create_type

from api.users.mutations.login import login
from api.users.mutations.register import register
from api.users.mutations.update_profile import update_profile
from api.users.mutations.request_reset_password import request_reset_password
from api.users.mutations.logout import logout


UsersMutations = create_type(
    "UsersMutations",
    [login, register, update_profile, request_reset_password, logout],
)
