from django.conf import settings
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth.models import AnonymousUser
from pythonit_toolkit.headers import PASTAPORTO_X_HEADER
from pythonit_toolkit.pastaporto.entities import Pastaporto
from pythonit_toolkit.pastaporto.exceptions import InvalidPastaportoError


def force_pycon_host(get_response):
    def middleware(request):
        request.META["HTTP_X_FORWARDED_PROTO"] = "https"
        request.META["HTTP_HOST"] = "pycon.it"

        return get_response(request)

    return middleware


class AnonymousPastaporto:
    @property
    def is_authenticated(self) -> bool:
        return False


def pastaporto_auth(get_response):
    def middleware(request):
        pastaporto_token = request.headers.get(PASTAPORTO_X_HEADER, None)

        if not pastaporto_token:
            request.pastaporto = AnonymousPastaporto()
            request.user = AnonymousUser()
            return get_response(request)

        try:
            pastaporto = Pastaporto.from_token(
                pastaporto_token, settings.PASTAPORTO_SECRET
            )
            request.pastaporto = pastaporto
            request.user = pastaporto.user_info or AnonymousUser()
        except InvalidPastaportoError as e:
            request.pastaporto = None
            request.user = None
            raise ValueError("Invalid pastaporto") from e

        return get_response(request)

    return middleware


class CustomAuthenticationMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        if request.path == "/graphql":
            # if we are on /graphql as path
            # we do not want to use this auth system
            return

        super().process_request(request)
