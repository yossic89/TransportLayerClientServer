from client.src.transport_client import UDPClient, TCPClient
from utilities import constants
from utilities.logger import Logger

logger = Logger.instance()


class ClientRunner(object):
    """
    runner for client
    run each time tcp or udp
    """
    def __init__(self, ip, port, timeout, packet_size, type):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.packet_size = packet_size
        self.type = type

    def run(self):
        if self.type == constants.UDP:
            client = UDPClient(self.ip, self.port, self.timeout, self.packet_size)
            client.run_client()
        elif self.type == constants.TCP:
            client = TCPClient(ip=self.ip, port=self.port, timeout=self.timeout, packet_size=self.packet_size)
            client.run_client()
