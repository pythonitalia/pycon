from temporalio.client import Client
from asgiref.sync import async_to_sync
from django.conf import settings


@async_to_sync
async def start_workflow(*args, **kwargs):
    client = await Client.connect(settings.TEMPORAL_ADDRESS)
    return await client.start_workflow(*args, **kwargs)
