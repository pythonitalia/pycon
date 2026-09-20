"""Run the Resonate worker: the process that executes durable workflows."""

import asyncio
import logging
import signal

from django.core.management.base import BaseCommand

from pycon.resonate_app import autodiscover_workflows, get_resonate

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run the Resonate worker, executing durable workflows"

    def handle(self, *args, **options):
        asyncio.run(self._run())

    async def _run(self):
        autodiscover_workflows()

        resonate = get_resonate()
        resonate.start()

        self.stdout.write(self.style.SUCCESS("Resonate worker started"))

        stop = asyncio.Event()
        loop = asyncio.get_running_loop()

        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, stop.set)

        try:
            await stop.wait()
        finally:
            self.stdout.write("Stopping Resonate worker")
            await resonate.stop()
