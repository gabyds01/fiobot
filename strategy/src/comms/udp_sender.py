import socket

import os

from proto.packet_pb2 import Packet

from dotenv import load_dotenv

load_dotenv()

MCAST_IP = os.getenv("MCAST_IP_OUT")
MCAST_PORT = int(os.getenv("MCAST_PORT_OUT"))


class UDPSender:
    def __init__(self):
        # Set up socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(
            socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1
        )  # Local subnet

    def send(self, data):
        self.sock.sendto(data, (MCAST_IP, MCAST_PORT))

    def serialize(self):
        packet = Packet()
        cmd = packet.cmd.robot_commands.add()
        cmd.id = 0
        cmd.yellowteam = False
        cmd.wheel_left = 10.0
        cmd.wheel_right = 10.0

        return packet.SerializeToString()


sender = UDPSender()
sender.send(sender.serialize())
