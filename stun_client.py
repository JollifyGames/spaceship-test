from typing import Tuple

import stun
import socket

# Declare the global socket variable
global global_socket


def get_ip_info() -> Tuple[str, str, int]:
    global global_socket
    global_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    nat_type, external_ip, external_port, global_socket = stun.get_ip_info(global_socket)
    return nat_type, external_ip, external_port
