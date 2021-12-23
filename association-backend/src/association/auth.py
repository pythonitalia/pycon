from pythonit_toolkit.starlette_backend.pastaporto_backend import PastaportoAuthBackend
from starlette.authentication import AuthenticationBackend

from src.association.settings import PASTAPORTO_SECRET
from src.webhooks.auth_backend import PretixAuthBackend


class RouterAuthBackend(AuthenticationBackend):
    def __init__(self):
        self.pretix_auth_backend = PretixAuthBackend()
        self.pastaporto_backend = PastaportoAuthBackend(PASTAPORTO_SECRET)

    async def authenticate(self, request):
        # Based on the path, use a different authentication method
        if request.url.path == "/pretix-webhook":
            return await self.pretix_auth_backend.authenticate(request)

        return await self.pastaporto_backend.authenticate(request)
