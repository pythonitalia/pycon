# This entire module is a WebSocket reverse proxy
# that forwards messages from the Vite HMR server to the client and vice-versa.
# The only reason we need it is because we need to alter the HMR messages
# to include the /astro prefix in the paths of the updates.
# This can be removed once Astro fully supports base paths.
import json
import asyncio
import websockets
import http


def modify_message(message):
    parsed_message = json.loads(message)
    if parsed_message["type"] == "update":
        updates = parsed_message["updates"]
        for update in updates:
            update["path"] = f"/astro{update['path']}"
            update["acceptedPath"] = f"/astro{update['acceptedPath']}"
    return json.dumps(parsed_message)


async def health_check(connection, request):
    if request.headers.get("Accept") == "text/x-vite-ping":
        return http.HTTPStatus.OK, [], b"OK\n"


async def handler(websocket):
    print("Connected", websocket.remote_address)

    async with websockets.connect(
        "ws://custom-admin:3002", subprotocols=["vite-hmr"]
    ) as server_ws:

        async def forward_to_client():
            try:
                async for message in server_ws:
                    modified_message = modify_message(message)
                    await websocket.send(modified_message)
            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed")

        async def forward_to_server():
            try:
                async for message in websocket:
                    await server_ws.send(message)
            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed")

        await asyncio.gather(forward_to_client(), forward_to_server())


async def main():
    async with websockets.serve(
        handler,
        "0.0.0.0",
        3003,
        process_request=health_check,
        subprotocols=["vite-hmr"],
    ):
        await asyncio.get_running_loop().create_future()


asyncio.run(main())
