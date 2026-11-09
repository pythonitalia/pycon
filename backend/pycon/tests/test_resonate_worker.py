import asyncio

import aiohttp
from aiohttp import web
from aiohttp.test_utils import TestServer
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from pytest import raises

from pycon.management.commands.resonate_worker import Command
from pycon.resonate_app import WorkerPollConnection


def test_worker_keeps_receiving_work_past_aiohttp_default_timeout(mocker):
    mocker.patch("aiohttp.client.DEFAULT_TIMEOUT", aiohttp.ClientTimeout(total=0.5))
    received = []

    async def stream(request):
        response = web.StreamResponse(headers={"Content-Type": "text/event-stream"})
        await response.prepare(request)
        await response.write(b"data: first\n\n")
        await asyncio.sleep(1)
        await response.write(b"data: second\n\n")
        await asyncio.sleep(5)
        return response

    async def listen():
        app = web.Application()
        app.router.add_get("/poll/{group}/{pid}", stream)
        async with TestServer(app) as server:
            connection = WorkerPollConnection(
                url=str(server.make_url("")), group="pycon"
            )
            connection.recv(received.append)
            await connection.start()
            await asyncio.sleep(1.5)
            await connection.stop()

    asyncio.run(listen())

    assert received == ["first", "second"]


def test_worker_reloads_on_code_changes_by_default(mocker, settings):
    settings.DEBUG = True
    settings.RESONATE_URL = "http://resonate:8001"

    mock_run_with_reloader = mocker.patch(
        "pycon.management.commands.resonate_worker.autoreload.run_with_reloader"
    )
    mock_run_worker = mocker.patch.object(Command, "run_worker")

    call_command("resonate_worker")

    mock_run_with_reloader.assert_called_once()
    mock_run_worker.assert_not_called()


def test_worker_does_not_reload_outside_debug(mocker, settings):
    settings.DEBUG = False
    settings.RESONATE_URL = "http://resonate:8001"

    mock_run_with_reloader = mocker.patch(
        "pycon.management.commands.resonate_worker.autoreload.run_with_reloader"
    )
    mock_run_worker = mocker.patch.object(Command, "run_worker")

    call_command("resonate_worker")

    mock_run_worker.assert_called_once()
    mock_run_with_reloader.assert_not_called()


def test_worker_reload_can_be_turned_off(mocker, settings):
    settings.DEBUG = True
    settings.RESONATE_URL = "http://resonate:8001"

    mock_run_with_reloader = mocker.patch(
        "pycon.management.commands.resonate_worker.autoreload.run_with_reloader"
    )
    mock_run_worker = mocker.patch.object(Command, "run_worker")

    call_command("resonate_worker", "--no-reload")

    mock_run_worker.assert_called_once()
    mock_run_with_reloader.assert_not_called()


def test_worker_needs_a_resonate_server(mocker, settings):
    settings.RESONATE_URL = ""

    mock_run_worker = mocker.patch.object(Command, "run_worker")

    with raises(ImproperlyConfigured):
        call_command("resonate_worker", "--no-reload")

    mock_run_worker.assert_not_called()
