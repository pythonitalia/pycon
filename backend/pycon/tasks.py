import time
import logfire
import boto3
from django.conf import settings
from pycon.celery_utils import OnlyOneAtTimeTask

from collections import Counter
from pycon.celery import app
from django.core.cache import cache
from django.utils import timezone


def _get_ecs_network_config():
    network_config = settings.ECS_NETWORK_CONFIG
    return {
        "subnets": network_config["subnets"],
        "securityGroups": network_config["security_groups"],
        "assignPublicIp": "ENABLED",
    }


@app.task(base=OnlyOneAtTimeTask)
def launch_heavy_processing_worker():
    if settings.ENVIRONMENT == "local":
        return

    cluster_name = f"pythonit-{settings.ENVIRONMENT}-heavy-processing-worker"
    ecs_client = boto3.client("ecs", region_name=settings.AWS_REGION_NAME)

    response = ecs_client.list_tasks(cluster=cluster_name, desiredStatus="RUNNING")

    if len(response["taskArns"]) > 0:
        return

    response = ecs_client.run_task(
        cluster=cluster_name,
        taskDefinition=f"pythonit-{settings.ENVIRONMENT}-heavy-processing-worker",
        count=1,
        networkConfiguration={"awsvpcConfiguration": _get_ecs_network_config()},
        launchType="FARGATE",
    )
    task_arn = response["tasks"][0]["taskArn"]
    attempts = 0

    while True:
        response = ecs_client.describe_tasks(cluster=cluster_name, tasks=[task_arn])

        if len(response["tasks"]) == 0:
            break

        last_status = response["tasks"][0]["lastStatus"]
        if last_status == "RUNNING":
            break

        if attempts > 10:
            logfire.error(
                "Heavy processing worker arn={task_arn} failed to start. Checked {attempts} times, giving up (last_status {last_status})",
                task_arn=task_arn,
                attempts=attempts,
                last_status=last_status,
            )
            break

        attempts += 1
        time.sleep(3 * attempts)


@app.task
def check_for_idle_heavy_processing_workers():
    inspect = app.control.inspect()
    workers_stats = inspect.stats()
    active_tasks = inspect.active()

    for worker_name, stats in workers_stats.items():
        if not worker_name.startswith("heavyprocessing"):
            continue

        cache_key = f"celery-workers-idle:{worker_name}"

        current_tasks = active_tasks.get(worker_name, [])
        if current_tasks:
            cache.delete(cache_key)
            continue

        current_jobs_executed = Counter(stats.get("total", {})).total()
        now = timezone.now()

        if last_check := cache.get(cache_key):
            last_check_jobs_executed = last_check["current_jobs_executed"]
            last_check_time = last_check["last_check"]

            if (now - last_check_time).total_seconds() < 300:
                # We haven't waited enough time to check again
                continue

            if last_check_jobs_executed == current_jobs_executed:
                logfire.info(
                    "Worker {worker_name} is idle, sending shutdown",
                    worker_name=worker_name,
                )
                app.control.broadcast("shutdown", destination=[worker_name])
                cache.delete(cache_key)
                continue

        logfire.info(
            "Worker {worker_name} total jobs executed: {current_jobs_executed}",
            worker_name=worker_name,
            current_jobs_executed=current_jobs_executed,
        )
        cache.set(
            cache_key,
            {
                "current_jobs_executed": current_jobs_executed,
                "last_check": now,
            },
            timeout=600,
        )
