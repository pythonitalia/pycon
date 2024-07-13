import logfire

from collections import Counter
from pycon.celery import app
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
