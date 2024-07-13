from pycon.tasks import launch_heavy_processing_worker


def test_launch_heavy_processing_worker_disabled_in_local_env(settings, mocker):
    settings.ENVIRONMENT = "local"

    mock_boto = mocker.patch("pycon.celery_utils.boto3")

    launch_heavy_processing_worker()

    assert not mock_boto.client.called


def test_launch_heavy_processing_worker_starts_task(settings, mocker):
    settings.ENVIRONMENT = "production"
    settings.ECS_NETWORK_CONFIG = {
        "subnets": ["a", "b"],
        "security_groups": ["sec1"],
    }

    mock_client = mocker.patch("pycon.celery_utils.boto3.client")
    mock_client.return_value.list_tasks.return_value = {"taskArns": []}

    launch_heavy_processing_worker()

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
    )


def test_launch_heavy_processing_worker_does_nothing_if_worker_is_running(
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
