import json
import os
import subprocess
import time

import boto3

services_to_deploy: list[str] = json.loads(os.environ["SERVICES"])
targets = []

for service in services_to_deploy:
    targets.append(f'-target module.{service.replace("-", "_")}')

result = subprocess.run(
    ["terraform", "apply", "-no-color", "-auto-approve", *targets],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)

logs = []
timestamp = int(time.time() * 1000)

logs.append({"timestamp": timestamp, "message": f"Terraform Apply logs"})

for line in result.stdout.splitlines():
    message = line.decode("utf-8")
    if not message:
        continue
    logs.append({"timestamp": timestamp, "message": message})


logs.append(
    {"timestamp": timestamp, "message": f"Terraform Exit code: {result.returncode}"}
)


client = boto3.client("logs")
client.create_log_stream(
    logGroupName=os.environ["CLOUDWATCH_LOG_GROUP"],
    logStreamName=os.environ["CLOUDWATCH_LOG_STREAM"],
)
response = client.put_log_events(
    logGroupName=os.environ["CLOUDWATCH_LOG_GROUP"],
    logStreamName=os.environ["CLOUDWATCH_LOG_STREAM"],
    logEvents=logs,
)
