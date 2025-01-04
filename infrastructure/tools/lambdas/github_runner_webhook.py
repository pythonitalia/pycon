import boto3
import json
import os
import hashlib
import hmac
from urllib import request

WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]
GITHUB_TOKEN_SSM_NAME = os.environ["GITHUB_TOKEN_SSM_NAME"]
NETWORK_CONFIGURATION = os.environ["NETWORK_CONFIGURATION"]


def handler(event, context):
    body = event.get("body").encode("utf-8")

    if not verify_signature(
        body, WEBHOOK_SECRET, event["headers"]["x-hub-signature-256"]
    ):
        return {"statusCode": 401, "body": ""}

    github_event = event["headers"]["x-github-event"]
    body = json.loads(body)

    match github_event:
        case "workflow_job":
            handle_workflow_job(body, context)
        case _:
            ...

    return {"statusCode": 200, "body": ""}


def handle_workflow_job(body, context):
    action = body["action"]

    if action != "queued":
        return

    workflow_job = body["workflow_job"]
    workflow_name = workflow_job["workflow_name"]

    if workflow_name != "Deploy":
        return

    labels = workflow_job["labels"]
    arm64_fargate_label = next(
        (label for label in labels if "arm64-fargate-" in label), None
    )
    if not arm64_fargate_label:
        return

    unique_run_id = arm64_fargate_label.replace("arm64-fargate-", "")

    ssm_client = boto3.client("ssm")
    github_token = ssm_client.get_parameter(Name=GITHUB_TOKEN_SSM_NAME)["Parameter"][
        "Value"
    ]

    payload = {
        "name": f"Runner for run #{unique_run_id}",
        "runner_group_id": 3,
        "labels": [arm64_fargate_label],
    }
    payload_encoded = json.dumps(payload).encode("utf-8")
    print("sending payload:", payload_encoded)
    req = request.Request(
        "https://api.github.com/orgs/pythonitalia/actions/runners/generate-jitconfig",
        data=payload_encoded,
        method="POST",
        headers={
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    with request.urlopen(req) as response:
        response_data = response.read().decode("utf-8")
        print(response_data)

    jit_config = json.loads(response_data)["encoded_jit_config"]

    print("Handling workflow job - start?", jit_config)
    print("Body:", body)
    print("Context:", context)

    ecs_client = boto3.client("ecs")
    ecs_client.start_task(
        cluster="github-actions-runners",
        networkConfiguration=json.loads(NETWORK_CONFIGURATION),
    )


def verify_signature(payload_body, secret_token, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        return False

    hash_object = hmac.new(
        secret_token.encode("utf-8"), msg=payload_body, digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()

    if not hmac.compare_digest(expected_signature, signature_header):
        return False

    return True
