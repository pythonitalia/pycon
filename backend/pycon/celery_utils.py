from celery import Task
import logging
from django.conf import settings
import hashlib
import os
import threading
from kombu.utils.encoding import safe_repr
import redis

logger = logging.getLogger(__name__)


def renew_lock(lock, interval, _stop_event):
    while not _stop_event.wait(timeout=interval):
        if not lock.locked:
            return

        if _stop_event.is_set():
            return

        try:
            lock.extend(interval, replace_ttl=True)
        except Exception as e:
            logger.exception("Error renewing lock: %s", e)
            break


def make_lock_id(func, *args):
    hash = hashlib.md5()
    for arg in args:
        if not isinstance(arg, str):
            arg = str(arg)
        hash.update(arg.encode("utf-8"))

    PYTEST_XDIST_WORKER = os.environ.get("PYTEST_XDIST_WORKER")
    key = f"celery_lock_{func.__module__}_{func.__name__}_{hash.hexdigest()}"

    if PYTEST_XDIST_WORKER:
        key = f"{key}_{PYTEST_XDIST_WORKER}"

    return key


class BaseTaskWithLock(Task):
    timeout = 60 * 5

    def __init__(self, *args, **kwargs):
        self.client = redis.Redis.from_url(settings.REDIS_URL)

    def acquire_lock(self, *args, **kwargs):
        lock_id = make_lock_id(self, *args)
        self.lock = self.client.lock(lock_id, timeout=self.timeout, thread_local=False)
        return self.lock.acquire(blocking=False)

    def __call__(self, *args, **kwargs):
        self.lock = None
        self._stop_event = None
        self.renewer_thread = None

        if not self.acquire_lock(*args, **kwargs):
            logger.info(
                "Task %s.%s[%s] is already running, skipping",
                self.__module__,
                self.__name__,
                ",".join([safe_repr(arg) for arg in args]),
            )
            return

        self._stop_event = threading.Event()

        self.renewer_thread = threading.Thread(
            target=renew_lock, args=(self.lock, self.timeout - 30, self._stop_event)
        )
        self.renewer_thread.daemon = True
        self.renewer_thread.start()

        return super().__call__(*args, **kwargs)

    def after_return(self, *args, **kwargs):
        if self.lock and self.lock.owned():
            self.lock.release()

        if self._stop_event:
            self._stop_event.set()

        if self.renewer_thread:
            self.renewer_thread.join()
