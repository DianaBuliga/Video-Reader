import asyncio
import websockets

from websocketServer.sharedState import SharedState


async def send_data_to_client(message):
    state = SharedState()
    print(f"message: {message}")
    clients_connected = state.get_clients()
    for client in clients_connected.copy():
        try:
            await asyncio.gather(*[
                client.send(message) for client in clients_connected
            ])
        except websockets.exceptions.ConnectionClosed:
            clients_connected.remove(client)

    await asyncio.sleep(0.04)  # ~25 fps
