import logging

import websocket
from websocket import WebSocket

import bot_behaviour
import data_classes
import stun_client
import udp_client
from data_classes import *

EAST_US_CLOUD_WS_URL = "ws://52.186.175.70:8080/room/"
EUROPE_CLOUD_BASE_URL = "ws://98.67.168.204:8080/room/"

T = TypeVar('T')

run_simulation = True


def on_open(ws):
    print("Opened connection")


def on_message(ws: WebSocket, message_json):
    global run_simulation

    try:
        generic_message = json.loads(message_json)
        command = convert_to_websocket_command(generic_message["Command"])

        if command is None:
            logging.error("Unrecognized command received")
            return

        print("Command is:", command)

        if command == WebSocketCommand.START:
            raw_message = generic_message["Payload"]
            print("Start game message:", raw_message)
            udp_client.start_listening(stun_client.global_socket)
            bot_behaviour.start_simulation_thread()
        elif command in [WebSocketCommand.WIN, WebSocketCommand.LOSE]:
            print("Game lost or won. the socket needs to be closed")
            run_simulation = False
            ws.close()

    except Exception as e:
        logging.error(f"Error processing message: {e}")


def on_error(ws, error):
    print("Error:", error)


def on_close(ws, close_status_code, close_msg):
    print("Closed:", close_status_code, close_msg)


def init_websocket(game_id, player_id):
    ws_url = f"{EUROPE_CLOUD_BASE_URL}{game_id}?playerId={player_id}"
    return websocket.WebSocketApp(ws_url,
                                  on_open=on_open,
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close)


def connect_websocket(game_id: str, player_id: str):
    ws = init_websocket(game_id=game_id, player_id=player_id)
    ws.run_forever()


def convert_to_websocket_command(command_value):
    try:
        return data_classes.WebSocketCommand(command_value)
    except ValueError:
        logging.error(f"Invalid WebSocket command: {command_value}")
        return None
