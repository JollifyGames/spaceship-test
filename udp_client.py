import threading
from socket import socket
import msgpack

import ws_client

EUROPE_VM_IP: str = "98.67.168.204"
EAST_US_VM_IP: str = "52.186.175.70"
UDP_PORT: int = 49999


def send_introductory_packet(sock: socket):
    payload = "intro"
    send_bytes = payload.encode('utf-8')
    sock.sendto(send_bytes, (EUROPE_VM_IP, UDP_PORT))


def _listen_udp_packets(sock: socket):
    while ws_client.run_simulation:
        try:
            data, addr = sock.recvfrom(1024)
            # print(f"Received message: {data} from {addr}")
        except Exception as e:
            print(f"Error receiving data: {e}")


def start_listening_udp_packets(sock: socket):
    listening_thread = threading.Thread(target=_listen_udp_packets, args=(sock,))
    listening_thread.daemon = True
    listening_thread.start()


def send_udp_message(global_socket: socket, send_bytes):
    try:
        global_socket.sendto(send_bytes, (EUROPE_VM_IP, UDP_PORT))
    except socket.timeout:
        print("Timeout occurred while sending UDP message")
    except Exception as e:
        print(f"Error sending UDP message: {e}")
