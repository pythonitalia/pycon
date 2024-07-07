from .celery import app


@app.task
def check_for_idle_heavy_processing_workers():
    ...
    # inspect = app.control.inspect()
    # active_tasks = inspect.active()

    # active_count = sum(
    #     len(tasks) for tasks in active_tasks.values()
    #     if 'heavy_processing' in [task['delivery_info']['routing_key'] for task in tasks]
    # ) if active_tasks else 0

    # for worker_name, tasks in active_tasks.items():
    #     if len(tasks) > 0:
    #         continue
    # pass
