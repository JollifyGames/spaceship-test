import json
from enum import Enum
from typing import Generic, TypeVar


class Game:
    def __init__(self, game_id, game_status, duration, game_code):
        self.game_id = game_id
        self.game_status = game_status
        self.duration = duration
        self.game_code = game_code

    def __str__(self):
        return f"Game {{ gameId: {self.game_id}, gameStatus: {self.game_status}, duration: {self.duration}, " \
               f"gameCode: {self.game_code} }}"


T = TypeVar('T')


class WebSocketCommand(Enum):
    START = 10
    OPPONENT_DISCONNECT = 11
    OPPONENT_RECONNECT = 12
    WIN = 98
    LOSE = 99


class WebSocketMessage(Generic[T]):
    def __init__(self, command: WebSocketCommand, game_id: str, payload: T):
        self.command = command
        self.game_id = game_id
        self.payload = payload


class StartWebSocketMessage:
    def __init__(self, timer_count=5):
        self.timer_count = timer_count
