import os
import subprocess
import time

import boto3

result = subprocess.run(
    ["terraform", "apply", "-no-color", "-auto-approve"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)


logs = []
timestamp = time.time()
for line in result.stdout.splitlines():
    logs.append({"timestamp": timestamp, "message": line})


client = boto3.client("logs")
client.put_log_events(
    logGroupName=os.environ["CLOUDWATCH_LOG_GROUP"],
    logStreamName=os.environ["CLOUDWATCH_STREAM_NAME"],
    logEvents=logs,
)
