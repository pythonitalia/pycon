import os
import hashlib
from pycon.celery_utils import launch_heavy_processing_worker, make_lock_id


def test_func():
    pass


def test_make_lock_id(mocker):
    mocker.patch.dict(os.environ, {"PYTEST_XDIST_WORKER": ""})
    key = make_lock_id(test_func)
    assert key == "celery_lock_pycon.tests.test_celery_utils_test_func"

    key = make_lock_id(test_func, 1, 2, 3)
    args_md5 = hashlib.md5("123".encode("utf-8")).hexdigest()
    assert key == f"celery_lock_pycon.tests.test_celery_utils_test_func_{args_md5}"

    mocker.patch.dict(os.environ, {"PYTEST_XDIST_WORKER": "1"})
    key = make_lock_id(test_func)
    assert key == "celery_lock_pycon.tests.test_celery_utils_test_func_1"


def test_launch_large_storage_worker_disabled_in_local_env(settings, mocker):
    settings.ENVIRONMENT = "local"

    mock_boto = mocker.patch("pycon.celery_utils.boto3")

    launch_heavy_processing_worker()

    assert not mock_boto.client.called


def test_launch_large_storage_worker_starts_task(settings, mocker):
    settings.ENVIRONMENT = "production"
    settings.ECS_NETWORK_CONFIG = {
        "subnets": ["a", "b"],
        "security_groups": ["sec1"],
    }

    mock_client = mocker.patch("pycon.celery_utils.boto3.client")
    mock_client.return_value.list_tasks.return_value = {"taskArns": []}

    launch_heavy_processing_worker()

    mock_client.return_value.list_tasks.assert_called_with(
        cluster="pythonit-production-large-storage-worker", desiredStatus="RUNNING"
    )

    mock_client.return_value.run_task.assert_called_with(
        cluster="pythonit-production-large-storage-worker",
        taskDefinition="pythonit-production-large-storage-worker",
        count=1,
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": ["a", "b"],
                "securityGroups": ["sec1"],
                "assignPublicIp": "ENABLED",
            }
        },
        launchType="FARGATE",
    )


def test_launch_large_storage_worker_does_nothing_if_worker_is_running(
    settings, mocker
):
    settings.ENVIRONMENT = "production"
    settings.ECS_NETWORK_CONFIG = {
        "subnets": ["a", "b"],
        "security_groups": ["sec1"],
    }

    mock_client = mocker.patch("pycon.celery_utils.boto3.client")
    mock_client.return_value.list_tasks.return_value = {"taskArns": ["arn-abc"]}

    launch_heavy_processing_worker()

    assert not mock_client.return_value.run_task.called
