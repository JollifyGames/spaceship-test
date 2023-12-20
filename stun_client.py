from typing import Tuple

import stun
import socket

global global_socket


def get_ip_info() -> Tuple[str, str, int]:
    global global_socket
    global_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    nat_type, external_ip, external_port = get_ip_info2(global_socket)
    return nat_type, external_ip, external_port


def get_ip_info2(s: socket.socket, source_ip="0.0.0.0", source_port=0,
                 stun_host=None, stun_port=3478):
    s.settimeout(2)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((source_ip, source_port))
    nat_type, nat = stun.get_nat_type(s, source_ip, source_port,
                                      stun_host=stun_host, stun_port=stun_port)
    external_ip = nat['ExternalIP']
    external_port = nat['ExternalPort']
    return nat_type, external_ip, external_port


def get_ip_port() -> Tuple[str, int]:
    global global_socket
    global_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    external_ip, external_port = get_ip_port2(global_socket)
    return external_ip, external_port


def get_ip_port2(s: socket.socket, source_ip="0.0.0.0", source_port=0,
                 stun_host=None, stun_port=3478):
    s.settimeout(2)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((source_ip, source_port))

    stun._initialize()
    nat = stun.stun_test(s, stun.STUN_SERVERS[0], stun_port, source_ip, source_port)
    external_ip = nat['ExternalIP']
    external_port = nat['ExternalPort']
    return external_ip, external_port
