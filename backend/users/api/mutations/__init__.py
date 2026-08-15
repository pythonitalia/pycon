from strawberry.tools import create_type

from users.api.mutations.login import login
from users.api.mutations.register import register
from users.api.mutations.update_profile import update_profile
from users.api.mutations.request_reset_password import request_reset_password
from users.api.mutations.logout import logout
from users.api.mutations.reset_password import reset_password

UsersMutations = create_type(
    "UsersMutations",
    [login, register, update_profile, reset_password, request_reset_password, logout],
)
