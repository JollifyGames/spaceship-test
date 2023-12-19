from typing import Optional


class Player:
    def __init__(self, player_id=""):
        self.player_id = player_id
    # Add other player attributes and methods as needed


class Game:
    def __init__(self, game_id=""):
        self.game_id = game_id
    # Add other game attributes and methods as needed


class BackEndDataManager:
    Player = Player()
    Game = Game()
    Port = 0
    IpAddress = None  # Assuming you have a way to represent IP addresses
    Duration = 3
    PacketCount = 0

    @classmethod
    def set_port(cls, port):
        cls.Port = port

    @classmethod
    def get_port(cls):
        return cls.Port

    @classmethod
    def set_ip_address(cls, ip_address):
        cls.IpAddress = ip_address

    @classmethod
    def get_ip_address(cls):
        return cls.IpAddress

    @classmethod
    def set_game_duration(cls, duration):
        cls.Duration = duration

    @classmethod
    def get_game_duration(cls):
        return cls.Duration

    @classmethod
    def get_player_id(cls):
        return cls.Player.player_id

    @classmethod
    def set_player_id(cls, player_id):
        cls.Player.player_id = player_id

    @classmethod
    def get_game_id(cls):
        return cls.Game.game_id

    @classmethod
    def set_game_id(cls, game_id):
        cls.Game.game_id = game_id

    @classmethod
    def get_packet_count(cls):
        return cls.PacketCount

    @classmethod
    def increment_packet_count(cls):
        cls.PacketCount += 1
