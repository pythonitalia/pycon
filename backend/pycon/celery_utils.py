import boto3
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
    key = f"celery_lock_{func.__module__}_{func.__name__}"

    hash = hashlib.md5()
    for arg in args:
        if not isinstance(arg, str):
            arg = str(arg)
        hash.update(arg.encode("utf-8"))

    if args:
        key = f"{key}_{hash.hexdigest()}"

    if xdist_worker := os.environ.get("PYTEST_XDIST_WORKER"):
        key = f"{key}_{xdist_worker}"

    return key


class OnlyOneAtTimeTask(Task):
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
            target=renew_lock, args=(self.lock, self.timeout / 2, self._stop_event)
        )
        self.renewer_thread.daemon = True
        self.renewer_thread.start()

        try:
            super().__call__(*args, **kwargs)
        finally:
            # Workaround for unit-tests to release the lock
            if settings.IS_RUNNING_TESTS:
                self.after_return()

    def after_return(self, *args, **kwargs):
        if self.lock and self.lock.owned():
            self.lock.release()

        if self._stop_event:
            self._stop_event.set()

        if self.renewer_thread:
            self.renewer_thread.join()


def _get_ecs_network_config():
    network_config = settings.ECS_NETWORK_CONFIG
    return {
        "subnets": network_config["subnets"],
        "securityGroups": network_config["security_groups"],
        "assignPublicIp": "ENABLED",
    }


def launch_large_storage_worker():
    if settings.ENVIRONMENT == "local":
        return

    cluster_name = f"pythonit-{settings.ENVIRONMENT}-large-storage-worker"
    ecs_client = boto3.client("ecs", region_name=settings.AWS_REGION_NAME)

    response = ecs_client.list_tasks(cluster=cluster_name, desiredStatus="RUNNING")

    if len(response["taskArns"]) > 0:
        return

    ecs_client.run_task(
        cluster=cluster_name,
        taskDefinition=f"pythonit-{settings.ENVIRONMENT}-large-storage-worker",
        count=1,
        networkConfiguration={"awsvpcConfiguration": _get_ecs_network_config()},
        launchType="FARGATE",
    )
