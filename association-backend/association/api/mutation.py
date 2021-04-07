from pythonit_toolkit.api.builder import create_root_type

from .mutations.create_subscription_session import create_subscription_session

Mutation = create_root_type([create_subscription_session])
