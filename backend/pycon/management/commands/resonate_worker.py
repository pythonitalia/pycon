"""Run the Resonate worker: the process that executes durable workflows."""

import asyncio
import atexit
import signal
import threading

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import autoreload

from pycon.resonate_app import autodiscover_workflows, get_resonate, require_server

# How long the worker is given to release its tasks when the autoreloader is
# about to replace the process.
SHUTDOWN_TIMEOUT_SECONDS = 5


class Command(BaseCommand):
    help = "Run the Resonate worker, executing durable workflows"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reload",
            action="store_true",
            dest="use_reloader",
            default=settings.DEBUG,
            help="Restart the worker when the code changes (the default with DEBUG)",
        )
        parser.add_argument(
            "--no-reload",
            action="store_false",
            dest="use_reloader",
            help="Do not restart the worker when the code changes",
        )

    def handle(self, *args, **options):
        # Fail before the reloader spawns a child that could only fail there,
        # where the error is a lot less visible.
        require_server()

        if options["use_reloader"]:
            autoreload.run_with_reloader(self.run_worker)
        else:
            self.run_worker()

    def run_worker(self):
        asyncio.run(self._run())

    async def _run(self):
        autodiscover_workflows()

        resonate = get_resonate()
        resonate.start()

        self.stdout.write(self.style.SUCCESS("Resonate worker started"))

        stop = asyncio.Event()
        stopped = threading.Event()
        self._stop_on_shutdown(stop, stopped)

        try:
            await stop.wait()
        finally:
            self.stdout.write("Stopping Resonate worker")
            await resonate.stop()
            stopped.set()

    def _stop_on_shutdown(self, stop: asyncio.Event, stopped: threading.Event):
        """Ask the worker to stop when the process is going away.

        Run directly, the worker owns the main thread and can take the signals
        itself. Under the autoreloader it instead runs in a daemon thread,
        while the reloader exits the process from the main thread on a code
        change -- so the worker stops from an exit hook, which still runs while
        the daemon thread is alive, rather than being killed mid-task.
        """
        loop = asyncio.get_running_loop()

        if threading.current_thread() is threading.main_thread():
            for sig in (signal.SIGINT, signal.SIGTERM):
                loop.add_signal_handler(sig, stop.set)
            return

        def on_exit():
            try:
                loop.call_soon_threadsafe(stop.set)
            except RuntimeError:
                # The loop is already gone; nothing left to stop.
                return

            stopped.wait(timeout=SHUTDOWN_TIMEOUT_SECONDS)

        atexit.register(on_exit)
