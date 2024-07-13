from collections import Counter
from .celery import app
from django.core.cache import cache


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

        total_jobs_executed = Counter(stats.get("total", {})).total()

        if cache.get(cache_key) == total_jobs_executed:
            app.control.broadcast("shutdown", destination=[worker_name])
            continue

        cache.set(cache_key, total_jobs_executed)
