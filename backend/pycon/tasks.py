from .celery import app
from django.core.cache import cache


@app.task
def check_for_idle_heavy_processing_workers():
    inspect = app.control.inspect()
    workers_stats = inspect.stats()
    active_tasks = inspect.active()

    for worker_name in workers_stats.keys():
        if not worker_name.startswith("heavyprocessing"):
            continue

        current_tasks = active_tasks.get(worker_name, [])
        if current_tasks:
            continue

        cache_key = f"celery-workers-idle:{worker_name}"

        if cache.get(cache_key) == "idle":
            app.control.broadcast("shutdown", destination=[worker_name])
            continue

        cache.set(cache_key, "idle", timeout=60 * 5)
