import os
import subprocess
import sys
import time

import boto3

result = subprocess.run(
    ["terraform", "apply", "-no-color", "-auto-approve"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)


logs = []
timestamp = int(time.time() * 1000)
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
    logStreamName=sys.argv[1],
)
response = client.put_log_events(
    logGroupName=os.environ["CLOUDWATCH_LOG_GROUP"],
    logStreamName=sys.argv[1],
    logEvents=logs,
)

print("response", response)
