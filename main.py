# main.py
import sys
from threading import Thread
import time

import rest_client
import stun_client
import udp_client
import ws_client
import back_end_data_manager


def on_play_game_button():
    # nat_type, external_ip, external_port = stun_client.get_ip_info()
    external_ip, external_port = stun_client.get_ip_port()
    player_id = rest_client.send_login_request()
    back_end_data_manager.BackEndDataManager.set_player_id(player_id)
    back_end_data_manager.BackEndDataManager.set_port(external_port)
    back_end_data_manager.BackEndDataManager.set_ip_address(external_ip)
    if player_id:
        game_response = rest_client.send_play_game_request(player_id=player_id, ip=external_ip, port=external_port)
        back_end_data_manager.BackEndDataManager.set_game_id(game_id=game_response.game_id)
        if game_response:
            udp_client.send_introductory_packet(stun_client.global_socket)
            ws_client.connect_websocket(game_id=game_response.game_id, player_id=player_id)
            return True
        else:
            print("Failed to get game response")
            return False
    else:
        print("Failed to get player ID")
        return False


def main():
    if on_play_game_button():
        print("Play game button triggered")
        try:
            while ws_client.run_simulation:
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("Shutting down...")
        print("The Game finished")


if __name__ == "__main__":
    main()
