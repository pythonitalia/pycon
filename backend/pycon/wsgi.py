import signal
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pycon.settings.prod")


def handle_sigterm(signum, frame):
    print("PyCon Received SIGTERM")
    with open("shutdown", "w") as f:
        f.write("shutdown")


try:
    signal.signal(signal.SIGTERM, handle_sigterm)
except ValueError:
    print("Could not set signal handler")


application = get_wsgi_application()
