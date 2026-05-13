import socket

import os
import struct

from dotenv import load_dotenv

load_dotenv()

MCAST_IP = os.getenv("MCAST_IP_IN")
MCAST_PORT = int(os.getenv("MCAST_PORT_IN"))


class UDPReceiver:
    def __init__(self):
        # Set up socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Join group with port
        self.mreq = struct.pack("4sl", socket.inet_aton(MCAST_IP), socket.INADDR_ANY)
        self.sock.bind((MCAST_IP, MCAST_PORT))
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self.mreq)

    def receive(self):
        data, addr = self.sock.recvfrom(1024)
        return data
