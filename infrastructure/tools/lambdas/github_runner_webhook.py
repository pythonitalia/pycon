import json
import os
import hashlib
import hmac

WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]


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
    if labels != ["self-hosted", "arm64-fargate"]:
        return

    print("Handling workflow job - start?")
    print("Body:", body)
    print("Context:", context)


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
