import asyncio
import json

from websocketServer.messages.message_handler import message_handler
from websocketServer.sharedState import SharedState
from websocketServer.websocketHandler.websocket_send import send_data_to_client


@message_handler("jumpToBeginning")
async def handle_jump_to_beginning(websocket, data):
    state = SharedState()
    state.set_video_position(0)
    await send_data_to_client(json.dumps({
            "type": 'player',
            "timeFrame": 0.0
        }))
