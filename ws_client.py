import logging
import time

import websocket
from websocket import WebSocket
import threading

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
    print("Ws Opened connection")


def on_message(ws: WebSocket, message_json):
    global run_simulation

    try:
        generic_message = json.loads(message_json)
        command = convert_to_websocket_command(generic_message["Command"])

        if command is None:
            logging.error("Unrecognized command received")
            return

        if command == WebSocketCommand.START:
            raw_message = generic_message["Payload"]
            print("Game Started")
            udp_client.start_listening(stun_client.global_socket)
            bot_behaviour.start_simulation_thread()
        elif command in [WebSocketCommand.WIN, WebSocketCommand.LOSE]:
            raw_message = generic_message["Payload"]
            print("Game Stopped")
            run_simulation = False

    except Exception as e:
        logging.error(f"Error processing message: {e}")


def on_error(ws, error):
    print("Ws Error:", error)


def on_close(ws, close_status_code, close_msg):
    print("Ws Closed:", close_status_code, close_msg)


def init_websocket(game_id, player_id):
    ws_url = f"{EUROPE_CLOUD_BASE_URL}{game_id}?playerId={player_id}"
    return websocket.WebSocketApp(ws_url,
                                  on_open=on_open,
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close)


def connect_websocket(game_id: str, player_id: str):
    ws = init_websocket(game_id=game_id, player_id=player_id)

    ws_thread = threading.Thread(target=lambda: ws.run_forever())
    ws_thread.daemon = True
    ws_thread.start()

    try:
        while run_simulation:
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Interrupt received, stopping...")
    ws.close()


def convert_to_websocket_command(command_value):
    try:
        return data_classes.WebSocketCommand(command_value)
    except ValueError:
        logging.error(f"Invalid WebSocket command: {command_value}")
        return None
