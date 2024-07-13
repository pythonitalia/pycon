import logfire

from collections import Counter
from .celery import app
from django.core.cache import cache
from django.utils import timezone


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

        last_check_value = cache.get(cache_key)
        if is_worker_idle(last_check_value, current_jobs_executed):
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


def is_worker_idle(last_check, current_jobs_executed):
    if not last_check:
        return False

    last_check_jobs_executed = last_check["current_jobs_executed"]
    last_check_time = last_check["last_check"]

    if (timezone.now() - last_check_time).total_seconds() < 300:
        return False

    # if the number of jobs didn't change in the last 5 mins
    # we consider the worker idle
    return last_check_jobs_executed == current_jobs_executed
