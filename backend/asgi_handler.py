import logging
import sys
import traceback
import sentry_sdk
from logging import getLogger
from mangum import Mangum
from django.apps import apps
from django.conf import settings
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from sentry_sdk.integrations.django import DjangoIntegration

logging.getLogger().setLevel(logging.INFO)
logger = getLogger(__name__)


SENTRY_DSN = settings.SENTRY_DSN

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            AwsLambdaIntegration(),
        ],
        traces_sample_rate=0.2,
        send_default_pii=True,
        environment=settings.ENVIRONMENT,
    )


def handler(event, context):
    if "Records" in event:
        logger.info("Received Records from lambda")
        apps.populate(settings.INSTALLED_APPS)
        from sqs_messages import process_sqs_messages

        process_sqs_messages(event)
        return

    if "_serverless-wsgi" in event:
        import shlex
        import subprocess

        from werkzeug._compat import StringIO, to_native

        native_stdout = sys.stdout
        native_stderr = sys.stderr
        output_buffer = StringIO()

        try:
            sys.stdout = output_buffer
            sys.stderr = output_buffer

            meta = event["_serverless-wsgi"]
            if meta.get("command") == "exec":
                # Evaluate Python code
                exec(meta.get("data", ""))
            elif meta.get("command2") == "command":
                # Run shell commands
                result = subprocess.check_output(
                    meta.get("data", ""), shell=True, stderr=subprocess.STDOUT
                )
                output_buffer.write(to_native(result))
            elif meta.get("command") == "manage":
                # Run Django management commands
                from django.core import management

                management.call_command(*shlex.split(meta.get("data", "")))
            else:
                raise Exception("Unknown command: {}".format(meta.get("command")))
        except subprocess.CalledProcessError as e:
            return [e.returncode, e.output.decode("utf-8")]
        except:  # noqa
            return [1, traceback.format_exc()]
        finally:
            sys.stdout = native_stdout
            sys.stderr = native_stderr

        return [0, output_buffer.getvalue()]
    else:
        from django.core.asgi import get_asgi_application

        asgi_handler = Mangum(get_asgi_application(), lifespan="off")
        return asgi_handler(event, context)
