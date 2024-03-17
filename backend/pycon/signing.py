from functools import wraps
from django.core.signing import Signer, BadSignature
from django.http import HttpResponseForbidden


def require_signed_request(view_func):
    @wraps(view_func)
    def _wrapper_view_func(request, *args, **kwargs):
        signer = Signer()
        # fallback to `sh` for backwards compatibility
        signature = request.GET.get("sig", request.GET.get("sh", None))

        if not signature:
            return HttpResponseForbidden("Missing signature.")

        try:
            signer.unsign(f"{request.path}:{signature}")
        except BadSignature:
            return HttpResponseForbidden("Invalid signature.")

        response = view_func(request, *args, **kwargs)
        return response

    return _wrapper_view_func


def sign_path(path: str):
    # TODO: Once we move the backend host under the correct domain
    # we can replace this with "sign_url"
    # and simplify the whole URL building process
    signer = Signer()
    signed_path = signer.sign(path)
    signature = signed_path.split(signer.sep)[-1]
    return f"{path}?sig={signature}"
