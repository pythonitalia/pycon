import requests
import time
import logging
from time import sleep
from django.conf import settings
from django.core.management.base import BaseCommand
from pycon.celery import app
from redis import Redis

logger = logging.getLogger(__name__)

QUEUE_NAME = "celery"
INTERVAL = 30


class Command(BaseCommand):
    def fetch_celery_data(self):
        self.celery_stats = app.control.inspect().stats() or {}
        self.celery_active = app.control.inspect().active() or {}

    def monitor(self):
        self.fetch_celery_data()
        metrics = {}
        tasks_in_queue = self.get_count_tasks_in_queue()
        metrics["tasks_in_queue"] = tasks_in_queue

        unhealthy_workers = []

        for worker_name, tasks in self.celery_active.items():
            if not tasks and tasks_in_queue:
                unhealthy_workers.append(worker_name)
                metrics[f"{worker_name}.unhealthy"] = 1
            else:
                metrics[f"{worker_name}.unhealthy"] = 0

            for task in tasks:
                task_name = task["name"]
                metric_count_name = f"{task_name}.count"
                metrics[metric_count_name] = metrics.get(metric_count_name, 0) + 1

        self.send_to_graphite(metrics)

    def handle(self, *args, **options):
        while True:
            try:
                self.monitor()
            except Exception:
                logger.exception("Error in monitor_celery_queues")
            sleep(INTERVAL)

    def get_count_tasks_in_queue(self):
        redis_instance = Redis.from_url(settings.CELERY_BROKER_URL)
        return redis_instance.llen(QUEUE_NAME)

    def send_to_graphite(self, metrics):
        payload = []
        for metric in metrics:
            payload.append(
                {
                    "name": f"pythonit.celery.{metric}",
                    "value": metrics[metric],
                    "time": int(time.time()),
                    "interval": INTERVAL,
                    "tags": [
                        f"env={settings.ENVIRONMENT}",
                    ],
                }
            )

        response = requests.post(
            "",
            json=payload,
            headers={
                "Authorization": "Bearer ",
            },
        )
        response.raise_for_status()
        pass
