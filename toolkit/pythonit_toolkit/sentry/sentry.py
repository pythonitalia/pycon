import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration


def strip_sensitive_data(event, hint):
    event["request"]["headers"].pop("x-pastaporto", "")
    return event


def configure_sentry(*, dsn: str, env: str):
    sentry_sdk.init(
        dsn=dsn,
        integrations=[AwsLambdaIntegration()],
        traces_sample_rate=0.1,
        environment=env,
        before_send=strip_sensitive_data,
    )
