# main.py
from threading import Thread
import time

import rest_client
import stun_client
import udp_client
import ws_client


def on_play_game_button():
    nat_type, external_ip, external_port = stun_client.get_ip_info()
    player_id = rest_client.send_login_request()

    if player_id:
        game_response = rest_client.send_play_game_request(player_id=player_id, ip=external_ip, port=external_port)

        if game_response:
            udp_client.send_introductory_packet(stun_client.global_socket)
            ws_thread = Thread(
                target=lambda: ws_client.connect_websocket(game_id=game_response.game_id, player_id=player_id))
            ws_thread.start()
            return True
        else:
            print("Failed to get game response")
            return False
    else:
        print("Failed to get player ID")
        return False


def main():
    if on_play_game_button():
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Shutting down...")


if __name__ == "__main__":
    main()
