import time_machine
from pycon.tasks import (
    build_idle_worker_cache_key,
    launch_heavy_processing_worker,
    check_for_idle_heavy_processing_workers,
)


def test_launch_heavy_processing_worker_disabled_in_local_env(settings, mocker):
    settings.ENVIRONMENT = "local"

    mock_boto = mocker.patch("pycon.tasks.boto3")

    launch_heavy_processing_worker()

    assert not mock_boto.client.called


def test_launch_heavy_processing_worker_starts_task(settings, mocker):
    mocker.patch("pycon.tasks.time")

    settings.ENVIRONMENT = "production"
    settings.ECS_NETWORK_CONFIG = {
        "subnets": ["a", "b"],
        "security_groups": ["sec1"],
    }

    mock_client = mocker.patch("pycon.tasks.boto3.client")
    mock_client.return_value.list_tasks.return_value = {"taskArns": []}
    mock_client.return_value.run_task.return_value = {"tasks": [{"taskArn": "arn-abc"}]}
    mock_client.return_value.describe_tasks.return_value = {
        "tasks": [
            {
                "lastStatus": "RUNNING",
            }
        ]
    }

    launch_heavy_processing_worker()

    mock_client.return_value.describe_tasks.assert_called_with(
        cluster="pythonit-production-heavy-processing-worker", tasks=["arn-abc"]
    )

    mock_client.return_value.list_tasks.assert_called_with(
        cluster="pythonit-production-heavy-processing-worker", desiredStatus="RUNNING"
    )

    mock_client.return_value.run_task.assert_called_with(
        cluster="pythonit-production-heavy-processing-worker",
        taskDefinition="pythonit-production-heavy-processing-worker",
        count=1,
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": ["a", "b"],
                "securityGroups": ["sec1"],
                "assignPublicIp": "ENABLED",
            }
        },
        launchType="FARGATE",
        enableExecuteCommand=True,
        startedBy="celery",
        volumeConfigurations=[
            {
                "name": "storage",
                "managedEBSVolume": {
                    "encrypted": False,
                    "sizeInGiB": 450,
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


def test_launch_heavy_processing_worker_waits_for_running_task(settings, mocker):
    mock_time = mocker.patch("pycon.tasks.time")

    settings.ENVIRONMENT = "production"
    settings.ECS_NETWORK_CONFIG = {
        "subnets": ["a", "b"],
        "security_groups": ["sec1"],
    }

    mock_client = mocker.patch("pycon.tasks.boto3.client")
    mock_client.return_value.list_tasks.return_value = {"taskArns": []}
    mock_client.return_value.run_task.return_value = {"tasks": [{"taskArn": "arn-abc"}]}
    mock_client.return_value.describe_tasks.return_value = {
        "tasks": [
            {
                "lastStatus": "PENDING",
            }
        ]
    }

    mock_client.return_value.describe_tasks.side_effect = [
        {"tasks": []},
        {
            "tasks": [
                {
                    "lastStatus": "PENDING",
                }
            ]
        },
        {
            "tasks": [
                {
                    "lastStatus": "RUNNING",
                }
            ]
        },
    ]

    launch_heavy_processing_worker()

    mock_time.sleep.assert_has_calls(
        [
            mocker.call(0),
            mocker.call(3),
            mocker.call(6),
        ]
    )


def test_launch_heavy_processing_worker_gives_up_waiting_start_after_10_attempts(
    settings, mocker
):
    mock_time = mocker.patch("pycon.tasks.time")

    settings.ENVIRONMENT = "production"
    settings.ECS_NETWORK_CONFIG = {
        "subnets": ["a", "b"],
        "security_groups": ["sec1"],
    }

    mock_client = mocker.patch("pycon.tasks.boto3.client")
    mock_client.return_value.list_tasks.return_value = {"taskArns": []}
    mock_client.return_value.run_task.return_value = {"tasks": [{"taskArn": "arn-abc"}]}
    mock_client.return_value.describe_tasks.return_value = {
        "tasks": [
            {
                "lastStatus": "PENDING",
            }
        ]
    }

    mock_client.return_value.describe_tasks.return_value = {
        "tasks": [
            {
                "lastStatus": "PENDING",
            }
        ]
    }

    launch_heavy_processing_worker()

    mock_time.sleep.assert_has_calls(
        [
            mocker.call(0),
            mocker.call(3),
            mocker.call(6),
            mocker.call(9),
            mocker.call(12),
            mocker.call(15),
            mocker.call(18),
            mocker.call(21),
            mocker.call(24),
            mocker.call(27),
            mocker.call(30),
        ]
    )


def test_launch_heavy_processing_worker_does_nothing_if_worker_is_running(
    settings, mocker
):
    settings.ENVIRONMENT = "production"
    settings.ECS_NETWORK_CONFIG = {
        "subnets": ["a", "b"],
        "security_groups": ["sec1"],
    }

    mock_client = mocker.patch("pycon.tasks.boto3.client")
    mock_client.return_value.list_tasks.return_value = {"taskArns": ["arn-abc"]}

    launch_heavy_processing_worker()

    assert not mock_client.return_value.run_task.called


def test_heavy_worker_is_flagged_for_possible_idle_if_doing_nothing(mocker):
    mock_cache = mocker.patch("pycon.tasks.cache")
    mock_cache.get.return_value = None

    mock_broadcast = mocker.patch("pycon.tasks.app.control.broadcast")
    mock_inspect = mocker.patch("pycon.tasks.app.control.inspect")
    mock_inspect.return_value.stats.return_value = {
        "normalworker@ip-1-2-3": {
            "total": {
                "task-name": 1,
            }
        },
        "heavyprocessing@ip-1-2-3": {
            "total": {
                "task-name": 3,
            }
        },
    }
    mock_inspect.return_value.active.return_value = {
        "normalworker@ip-1-2-3": [{"name": "task-name"}],
        "heavyprocessing@ip-1-2-3": [],
    }

    with time_machine.travel("2021-09-01 12:00:00", tick=False):
        check_for_idle_heavy_processing_workers()

    cache_key = build_idle_worker_cache_key("heavyprocessing@ip-1-2-3")
    mock_cache.set.assert_called_once_with(
        cache_key,
        {
            "current_jobs_executed": 3,
            "last_check": "2021-09-01T12:00:00+00:00",
        },
        timeout=600,
    )
    mock_broadcast.assert_not_called()


def test_idle_heavy_worker_is_shutdown_if_doing_nothing(mocker):
    mock_cache = mocker.patch("pycon.tasks.cache")
    mock_cache.get.return_value = {
        "current_jobs_executed": 3,
        "last_check": "2021-09-01T12:00:00+00:00",
    }

    mock_broadcast = mocker.patch("pycon.tasks.app.control.broadcast")
    mock_inspect = mocker.patch("pycon.tasks.app.control.inspect")
    mock_inspect.return_value.stats.return_value = {
        "normalworker@ip-1-2-3": {
            "total": {
                "task-name": 1,
            }
        },
        "heavyprocessing@ip-1-2-3": {
            "total": {
                "task-name": 3,
            }
        },
    }
    mock_inspect.return_value.active.return_value = {
        "normalworker@ip-1-2-3": [{"name": "task-name"}],
        "heavyprocessing@ip-1-2-3": [],
    }

    with time_machine.travel("2021-09-01 12:10:00", tick=False):
        check_for_idle_heavy_processing_workers()

    cache_key = build_idle_worker_cache_key("heavyprocessing@ip-1-2-3")
    mock_cache.delete.assert_called_once_with(cache_key)
    mock_broadcast.assert_called_once_with(
        "shutdown",
        destination=["heavyprocessing@ip-1-2-3"],
    )


def test_idle_heavy_worker_last_check_is_updated_if_jobs_count_changed(mocker):
    mock_cache = mocker.patch("pycon.tasks.cache")
    mock_cache.get.return_value = {
        "current_jobs_executed": 3,
        "last_check": "2021-09-01T12:00:00+00:00",
    }

    mock_broadcast = mocker.patch("pycon.tasks.app.control.broadcast")
    mock_inspect = mocker.patch("pycon.tasks.app.control.inspect")
    mock_inspect.return_value.stats.return_value = {
        "normalworker@ip-1-2-3": {
            "total": {
                "task-name": 1,
            }
        },
        "heavyprocessing@ip-1-2-3": {
            "total": {
                "task-name": 6,
                "another-task": 1,
            }
        },
    }
    mock_inspect.return_value.active.return_value = {
        "normalworker@ip-1-2-3": [{"name": "task-name"}],
        "heavyprocessing@ip-1-2-3": [],
    }

    with time_machine.travel("2021-09-01 12:10:00", tick=False):
        check_for_idle_heavy_processing_workers()

    cache_key = build_idle_worker_cache_key("heavyprocessing@ip-1-2-3")
    mock_cache.set.assert_called_once_with(
        cache_key,
        {
            "current_jobs_executed": 7,
            "last_check": "2021-09-01T12:10:00+00:00",
        },
        timeout=600,
    )
    mock_broadcast.assert_not_called()


def test_idle_heavy_worker_is_unmarked_as_idle_if_running_tasks(mocker):
    mock_cache = mocker.patch("pycon.tasks.cache")
    mock_cache.get.return_value = {
        "current_jobs_executed": 3,
        "last_check": "2021-09-01T12:00:00+00:00",
    }

    mock_broadcast = mocker.patch("pycon.tasks.app.control.broadcast")
    mock_inspect = mocker.patch("pycon.tasks.app.control.inspect")
    mock_inspect.return_value.stats.return_value = {
        "normalworker@ip-1-2-3": {
            "total": {
                "task-name": 1,
            }
        },
        "heavyprocessing@ip-1-2-3": {
            "total": {
                "task-name": 3,
            }
        },
    }
    mock_inspect.return_value.active.return_value = {
        "normalworker@ip-1-2-3": [{"name": "task-name"}],
        "heavyprocessing@ip-1-2-3": [
            {
                "name": "another-task",
            }
        ],
    }

    with time_machine.travel("2021-09-01 12:10:00", tick=False):
        check_for_idle_heavy_processing_workers()

    cache_key = build_idle_worker_cache_key("heavyprocessing@ip-1-2-3")
    mock_cache.delete.assert_called_once_with(
        cache_key,
    )
    mock_broadcast.assert_not_called()


def test_dont_shutdown_heavy_processing_worker_if_last_check_is_not_5_mins_old(mocker):
    mock_cache = mocker.patch("pycon.tasks.cache")
    mock_cache.get.return_value = {
        "current_jobs_executed": 3,
        "last_check": "2021-09-01T12:10:00+00:00",
    }

    mock_broadcast = mocker.patch("pycon.tasks.app.control.broadcast")
    mock_inspect = mocker.patch("pycon.tasks.app.control.inspect")
    mock_inspect.return_value.stats.return_value = {
        "normalworker@ip-1-2-3": {
            "total": {
                "task-name": 1,
            }
        },
        "heavyprocessing@ip-1-2-3": {
            "total": {
                "task-name": 3,
            }
        },
    }
    mock_inspect.return_value.active.return_value = {
        "normalworker@ip-1-2-3": [{"name": "task-name"}],
        "heavyprocessing@ip-1-2-3": [],
    }

    with time_machine.travel("2021-09-01 12:11:00", tick=False):
        check_for_idle_heavy_processing_workers()

    mock_cache.set.assert_not_called()
    mock_broadcast.assert_not_called()
