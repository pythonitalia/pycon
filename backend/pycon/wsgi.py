import logging
import signal
import os

from django.core.wsgi import get_wsgi_application

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pycon.settings.prod")


def handle_sigterm(signum, frame):
    logger.info("Received SIGTERM, shutting down")

    with open("shutdown", "w") as f:
        f.write("1")


try:
    signal.signal(signal.SIGTERM, handle_sigterm)
except ValueError:
    ...


application = get_wsgi_application()
