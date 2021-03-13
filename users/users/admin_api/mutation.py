from pythonit_toolkit.api.builder import create_root_type

from .mutations.login import login

Mutation = create_root_type([login])
