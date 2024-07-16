from pycon.celery import init_celery_tracing


def test_init_celery_tracing_does_not_crash():
    init_celery_tracing()
