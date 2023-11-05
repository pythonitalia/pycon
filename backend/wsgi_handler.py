#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copied from: https://github.com/dougmoscrop/serverless-http

This module loads the WSGI application specified by FQN
in `.serverless-wsgi` and invokes
the request when the handler is called by AWS Lambda.
Author: Logan Raarup <logan@logan.dk>
"""
import importlib
import logging
import os
import sys
import traceback
from logging import getLogger

import sentry_sdk
from django.apps import apps
from django.conf import settings
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.strawberry import StrawberryIntegration

# imports serverless_wsgi from the root
import serverless_wsgi

logging.getLogger().setLevel(logging.INFO)
logger = getLogger(__name__)


SENTRY_DSN = settings.SENTRY_DSN

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            AwsLambdaIntegration(),
            StrawberryIntegration(async_execution=False),
        ],
        traces_sample_rate=0.2,
        send_default_pii=True,
        environment=settings.ENVIRONMENT,
    )


def import_app(config):
    """Load the application WSGI handler"""
    wsgi_fqn = config["app"].rsplit(".", 1)
    wsgi_fqn_parts = wsgi_fqn[0].rsplit("/", 1)

    if len(wsgi_fqn_parts) == 2:
        root = os.path.abspath(os.path.dirname(__file__))
        sys.path.insert(0, os.path.join(root, wsgi_fqn_parts[0]))

    try:
        wsgi_module = importlib.import_module(wsgi_fqn_parts[-1])

        return getattr(wsgi_module, wsgi_fqn[1])
    except:  # noqa
        traceback.print_exc()
        raise Exception("Unable to import {}".format(config["app"]))


def handler(event, context):
    if "Records" in event:
        logger.info("Received Records from lambda")
        apps.populate(settings.INSTALLED_APPS)
        from sqs_messages import process_sqs_messages

        process_sqs_messages(event)
        return

    if "cronEvent" in event:
        logger.info("Received cronEvent from lambda")
        apps.populate(settings.INSTALLED_APPS)
        from association_membership.handlers import run_handler

        received_event = event["cronEvent"]
        run_handler("crons", received_event["name"], received_event["payload"])
        return

    """Lambda event handler, invokes the WSGI wrapper and handles command invocation"""
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
        return serverless_wsgi.handle_request(wsgi_app, event, context)


config = {"app": "pycon.wsgi.application"}
wsgi_app = import_app(config)
