# rest_client.py
import json
import uuid
from typing import Optional

import requests

from data_classes import Game

EUROPE_CLOUD_BASE_URL = 'http://98.67.168.204:8080/api/v1'
EAST_US_CLOUD_BASE_URL = 'http://52.186.175.70:8080/api/v1'


def generate_random_uuid():
    return str(uuid.uuid4())


def send_login_request() -> Optional[str]:
    url = EUROPE_CLOUD_BASE_URL + "/login"
    headers = {'Content-Type': 'application/json'}
    random_uuid = generate_random_uuid()
    payload = json.dumps({"DeviceId": random_uuid})

    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        player_data = response.json().get("Player")
        if player_data:
            player_id = player_data.get("PlayerId")
            return player_id
    return None


def send_play_game_request(player_id: str, ip: str, port: int) -> Optional[Game]:
    url = f"{EUROPE_CLOUD_BASE_URL}/{player_id}/join"
    headers = {'Content-Type': 'application/json'}
    payload = {
        'HostName': ip,
        'Port': port
    }
    response = requests.put(url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        game_data = response.json()
        game = Game(game_data.get('GameId'),
                    game_data.get('GameStatus'),
                    game_data.get('Duration'),
                    game_data.get('GameCode'))
        return game
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")
