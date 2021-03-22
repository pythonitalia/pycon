from pythonit_toolkit.api.builder import create_root_type

from .mutations.login import login
from .mutations.register import register
from .mutations.request_reset_password import request_reset_password
from .mutations.reset_password import reset_password

Mutation = create_root_type([login, register, request_reset_password, reset_password])
