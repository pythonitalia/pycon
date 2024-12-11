import sys
import signal
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pycon.settings.prod")


def handle_sigterm(signum, frame):
    with open("shutdown", "w") as f:
        f.write("shutdown")

    sys.exit(0)


try:
    signal.signal(signal.SIGTERM, handle_sigterm)
except ValueError:
    ...


application = get_wsgi_application()
