import asyncio
import logging

import websockets

from websocketServer.sharedState import SharedState


async def send_data_to_client(message):
    state = SharedState()
    clients_connected = state.get_clients()
    for client in clients_connected.copy():
        try:
            await asyncio.gather(*[
                client.send(message) for client in clients_connected
            ])
            logging.info('Send message to client')

        except websockets.exceptions.ConnectionClosed:
            clients_connected.remove(client)
            logging.warning(f'Client disconnected {client}')

    await asyncio.sleep(0.01)
