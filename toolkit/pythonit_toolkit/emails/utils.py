import importlib

from .backends.base import EmailBackend

EMAIL_BACKEND_CACHE: dict[str, EmailBackend] = {}


def get_email_backend(backend_path: str, **options: dict[str, str]) -> EmailBackend:
    global EMAIL_BACKEND_CACHE

    instance = EMAIL_BACKEND_CACHE.get(backend_path, None)

    if not instance:
        module_path, class_name = backend_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        class_impl = getattr(module, class_name)
        instance = class_impl(**options)
        EMAIL_BACKEND_CACHE[backend_path] = instance

    return instance
