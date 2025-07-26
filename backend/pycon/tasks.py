import time
import logging
import boto3
from django.conf import settings
from pycon.celery_utils import OnlyOneAtTimeTask
from redis import Redis
from collections import Counter
from pycon.celery import app
from django.core.cache import cache
from django.utils import timezone


logger = logging.getLogger(__name__)


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

    cluster_name = f"pythonit-{settings.ENVIRONMENT}"
    ecs_client = boto3.client("ecs", region_name=settings.AWS_REGION_NAME)

    response = ecs_client.list_tasks(
        cluster=cluster_name,
        desiredStatus="RUNNING",
        family=f"pythonit-{settings.ENVIRONMENT}-heavy-processing-worker",
    )

    if len(response["taskArns"]) > 0:
        return

    response = ecs_client.run_task(
        cluster=cluster_name,
        taskDefinition=f"pythonit-{settings.ENVIRONMENT}-heavy-processing-worker",
        count=1,
        networkConfiguration={"awsvpcConfiguration": _get_ecs_network_config()},
        launchType="FARGATE",
        enableExecuteCommand=True,
        startedBy="celery",
        volumeConfigurations=[
            {
                "name": "storage",
                "managedEBSVolume": {
                    "encrypted": False,
                    "sizeInGiB": 500,
                    "volumeType": "gp3",
                    "terminationPolicy": {"deleteOnTermination": True},
                    "filesystemType": "xfs",
                    "roleArn": settings.ECS_SERVICE_ROLE,
                    "iops": 16_000,
                    "throughput": 1_000,
                },
            }
        ],
    )
    task_arn = response["tasks"][0]["taskArn"]
    attempts = 0
    last_status = None

    while True:
        if attempts > 10:
            logger.error(
                "Heavy processing worker arn=%s failed to start. Checked %s times, giving up (last_status %s)",
                task_arn,
                attempts,
                last_status,
            )
            break

        time.sleep(3 * attempts)
        attempts += 1
        response = ecs_client.describe_tasks(cluster=cluster_name, tasks=[task_arn])
        response_tasks = response["tasks"]

        if not response_tasks:
            logger.warning(
                "Heavy processing worker arn=%s was started but describe_tasks returned no tasks [attempt=%s]",
                task_arn,
                attempts,
            )
            continue

        last_status = response_tasks[0]["lastStatus"]
        if last_status == "RUNNING":
            logger.info(
                "Heavy processing worker arn=%s running",
                task_arn,
            )
            break


@app.task(base=OnlyOneAtTimeTask)
def check_for_idle_heavy_processing_workers():
    inspect = app.control.inspect()
    workers_stats = inspect.stats()
    active_tasks = inspect.active()

    for worker_name, stats in workers_stats.items():
        if not worker_name.startswith("heavyprocessing"):
            continue

        cache_key = build_idle_worker_cache_key(worker_name)

        current_tasks = active_tasks.get(worker_name, [])
        if current_tasks:
            cache.delete(cache_key)
            continue

        current_jobs_executed = Counter(stats.get("total", {})).total()
        now = timezone.now()

        if last_check := cache.get(cache_key):
            last_check_jobs_executed = last_check["current_jobs_executed"]
            last_check_time = timezone.datetime.fromisoformat(last_check["last_check"])

            if (now - last_check_time).total_seconds() < 300:
                # We haven't waited enough time to check again
                continue

            if last_check_jobs_executed == current_jobs_executed:
                logger.info(
                    "Worker %s is idle, sending shutdown",
                    worker_name,
                )
                app.control.broadcast("shutdown", destination=[worker_name])
                cache.delete(cache_key)
                continue

        logger.info(
            "Worker %s total jobs executed: %s",
            worker_name,
            current_jobs_executed,
        )
        cache.set(
            cache_key,
            {
                "current_jobs_executed": current_jobs_executed,
                "last_check": now.isoformat(),
            },
            timeout=600,
        )


def build_idle_worker_cache_key(worker_name: str) -> str:
    return f"celery-workers-idle:{worker_name}"


@app.task(base=OnlyOneAtTimeTask)
def check_pending_heavy_processing_work():
    redis = Redis.from_url(settings.CELERY_BROKER_URL)
    tasks_in_queue = redis.llen("heavy_processing")

    if tasks_in_queue == 0:
        return

    launch_heavy_processing_worker.delay()
