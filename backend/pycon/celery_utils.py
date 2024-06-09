import logging
from django.conf import settings
import hashlib
import os
import threading

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
    return f"celery_lock_{func.__module__}_{func.__name__}_{hash.hexdigest()}"


def lock_task(func):
    # This is a dummy lock until we can get celery-heimdall
    def wrapper(*args, **kwargs):
        timeout = 60 * 5
        _stop_event = threading.Event()
        lock_id = make_lock_id(func, *args)
        PYTEST_XDIST_WORKER = os.environ.get("PYTEST_XDIST_WORKER")

        if PYTEST_XDIST_WORKER:
            lock_id = f"{lock_id}_{PYTEST_XDIST_WORKER}"

        client = redis.Redis.from_url(settings.REDIS_URL)
        lock = client.lock(lock_id, timeout=timeout, thread_local=False)

        if lock.acquire(blocking=False):
            renewer_thread = threading.Thread(
                target=renew_lock, args=(lock, timeout, _stop_event)
            )
            renewer_thread.daemon = True
            renewer_thread.start()

            try:
                return func(*args, **kwargs)
            finally:
                lock.release()
                _stop_event.set()
                renewer_thread.join()
        else:
            logger.info("Task %s is already running, skipping", func.__name__)
            return

    return wrapper
