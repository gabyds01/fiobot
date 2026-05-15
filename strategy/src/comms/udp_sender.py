import socket

import os

from proto.packet_pb2 import Packet

from engine.commands import RobotCommand

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

    def serialize(self, commands: list[RobotCommand]):
        packet = Packet()

        for robot_command in commands:
            cmd = packet.cmd.robot_commands.add()
            cmd.id = robot_command.robot_id
            cmd.yellowteam = robot_command.yellow_team
            cmd.wheel_left = robot_command.wheel_left
            cmd.wheel_right = robot_command.wheel_right

        return packet.SerializeToString()
