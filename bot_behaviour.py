import json
import random
import uuid

import udp_client


def simulate_ship_movement():
    move_x = random.uniform(-1, 1)
    move_y = random.uniform(-1, 1)
    move_intent = {
        "HorizontalMovement": move_x,
        "VerticalMovement": move_y,
        "PlayerId": PLAYER_ID
    }
    json_intent = json.dumps(move_intent)
    udp_client.send_udp_message()
    # send_udp_message(f"{INTENT_MOVE}|{json_intent}")


def simulate_ship_shoot_laser():
    laser_id = str(uuid.uuid4())
    shoot_intent = {
        "LaserId": laser_id,
        "PlayerId": PLAYER_ID
    }
    json_intent = json.dumps(shoot_intent)
    # send_udp_message(f"{INTENT_SHOOT_LASER}|{json_intent}")