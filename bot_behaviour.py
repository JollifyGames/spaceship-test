import json
import random
import threading
import time
import uuid

import back_end_data_manager
import stun_client
import udp_client
import ws_client
from UniqueIdGenerator import CommandIdGenerator
from back_end_data_manager import BackEndDataManager
from datetime import datetime
import tzlocal


def simulate_ship_movement():
    intent_type = "BB"
    move_x = random.uniform(-1, 1)
    move_y = random.uniform(-1, 1)
    local_tz = tzlocal.get_localzone()
    aware_datetime = datetime.now(local_tz)
    datetime_str = aware_datetime.isoformat()

    move_intent = {
        "HorizontalMovement": move_x,
        "VerticalMovement": move_y,
        "PlayerId": back_end_data_manager.BackEndDataManager.get_player_id(),
        "CommandId": CommandIdGenerator.generate_unique_command_id(),
        "Timestamp": datetime_str
    }
    json_intent = json.dumps(move_intent)

    packet_count = back_end_data_manager.BackEndDataManager.get_packet_count()
    game_id = back_end_data_manager.BackEndDataManager.get_game_id()
    payload = f"{packet_count}|{game_id}|{intent_type}|{json_intent}"

    send_bytes = payload.encode('utf-8')
    udp_client.send_udp_message(stun_client.global_socket, send_bytes)
    back_end_data_manager.BackEndDataManager.increment_packet_count()


def simulate_ship_shoot_laser():
    intent_type = "BC"
    local_tz = tzlocal.get_localzone()
    aware_datetime = datetime.now(local_tz)
    datetime_str = aware_datetime.isoformat()
    laser_id = str(uuid.uuid4())
    shoot_intent = {
        "LaserId": laser_id,
        "PlayerId": BackEndDataManager.get_player_id(),
        "CommandId": CommandIdGenerator.generate_unique_command_id(),
        "Timestamp": datetime_str
    }
    json_intent = json.dumps(shoot_intent)
    packet_count = back_end_data_manager.BackEndDataManager.get_packet_count()
    game_id = back_end_data_manager.BackEndDataManager.get_game_id()
    payload = f"{packet_count}|{game_id}|{intent_type}|{json_intent}"
    send_bytes = payload.encode('utf-8')
    udp_client.send_udp_message(stun_client.global_socket, send_bytes)
    back_end_data_manager.BackEndDataManager.increment_packet_count()


def _run_simulation():
    while ws_client.run_simulation:
        random_function = random.choice([simulate_ship_movement, simulate_ship_shoot_laser])
        random_function()
        # Wait for 25 milliseconds
        time.sleep(0.025)


def start_simulation_thread():
    simulation_thread = threading.Thread(target=_run_simulation)
    simulation_thread.daemon = True
    simulation_thread.start()
