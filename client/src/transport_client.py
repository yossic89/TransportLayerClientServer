from abc import ABCMeta, abstractmethod
from utilities.logger import Logger
import socket

logger = Logger.instance()


class TransportClient(metaclass=ABCMeta):
    """
    Abstract class for client
    """
    def __init__(self, ip, port, timeout, packet_size):
        self.ip = ip
        self.port = int(port)
        self.timeout = int(timeout) if timeout is not None else None
        self.packet_size = int(packet_size)

    # abstract methods
    @abstractmethod
    def _init(self):
        pass

    @abstractmethod
    def _send(self):
        pass

    @abstractmethod
    def _wait_for_response(self):
        pass

    def run_client(self):
        if not self._init():
            return False

        if not self._send():
            return False

        if not self._wait_for_response():
            return False

        return True


class TCPClient(TransportClient):
    """
    Class to run tcp client
    """
    def __init__(self, ip, port, timeout, packet_size):
        super().__init__(ip, port, timeout, packet_size)
        self.tcp_client = None

    def _init(self):
        try:
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_client.connect((self.ip, self.port))

            if self.timeout is not None:
                self.tcp_client.settimeout(self.timeout)
        except Exception as e:
            logger.log("TCP Client: failed to init client {}".format(str(e)))
            return False
        return True

    def _send(self):
        try:
            msg = 'A' * self.packet_size
            self.tcp_client.sendall(str.encode(msg))
        except Exception as e:
            logger.log("TCP Client: failed to send msg: {}".format(str(e)))
            return False
        return True

    def _wait_for_response(self):
        try:
            amount_received = 0
            amount_expected = self.packet_size

            while amount_received < amount_expected:
                data = self.tcp_client.recv(16)
                amount_received += len(data)

            logger.log("TCP Client: get response from server in size of {}".format(amount_received))
        except Exception as e:
            logger.log("TCP Client: Failed to receive data {}".format(str(e)))


class UDPClient(TransportClient):
    """
    Class for UDP Client
    """
    def __init__(self, ip, port, timeout, packet_size):
        super().__init__(ip, port, timeout, packet_size)
        self.udp_client = None
        self.server = (self.ip, self.port)

    def _init(self):
        try:
            self.udp_client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            if self.timeout is not None:
                self.udp_client.settimeout(self.timeout)
        except Exception as e:
            logger.log("UDP Client: failed to init client {}".format(str(e)))
            return False
        return True

    def _send(self):
        try:
            # create msg by given size
            msg = "A" * self.packet_size
            # send msg
            self.udp_client.sendto(str.encode(msg), self.server)
            return True
        except Exception as e:
            logger.log("UDP Client: failed to send msg: {}".format(str(e)))
            return False

    def _wait_for_response(self):
        try:
            msg = self.udp_client.recvfrom(self.packet_size)[0]
            logger.log("UDP Client: get response from server in size of {}".format(len(msg)))
        except Exception as e:
            logger.log("UDP Client: Failed to receive data {}".format(str(e)))
            return False
        return True
