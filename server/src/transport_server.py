from abc import ABCMeta, abstractmethod
from utilities.logger import Logger
import socket

logger = Logger.instance()


class TransportServer(metaclass=ABCMeta):
    """
    Abstract class for Server
    """
    def __init__(self, ip, port, buffer_size):
        self.ip = ip
        self.port = int(port)
        self.buffer_size = int(buffer_size)

    # abstract methods
    @abstractmethod
    def _init(self):
        pass

    @abstractmethod
    def _send_response(self):
        pass

    @abstractmethod
    def _wait_for_data(self):
        pass

    def run_server(self):
        if not self._init():
            return

        while True:
            try:
                if not self._wait_for_data():
                    continue
                self._send_response()
            except Exception as e:
                logger.log("Failed to run server {}, run again".format(str(e)))


class TCPServer(TransportServer):
    """
    TCP Server class
    """
    def __init__(self, ip, port, buffer_size):
        super().__init__(ip=ip, port=port, buffer_size=buffer_size)
        self.tcp_server = None
        self.client_packet_size = 0
        self.client_connection = None
        self.client_address = None

    def _init(self):
        try:
            self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_server.bind((self.ip, self.port))
        except Exception as e:
            logger.log("TCP Server: Failed to init tcp server: {}".format(str(e)))
            return False
        return True

    def _wait_for_data(self):
        try:
            # clean prev connection
            self.client_connection = None
            # wait for tcp data
            self.tcp_server.listen(1)
            self.client_connection, self.client_address = self.tcp_server.accept()

            # get data by buffer size - in case of client packet size bigger than server buffer, the process will fail
            data = self.client_connection.recv(self.buffer_size)
            self.client_packet_size = len(data)
            logger.log("TCP Server: get data from {} in size of {}".format(self.client_address, self.client_packet_size))
        except Exception as e:
            logger.log("TCP Server: Failed to receive data: {}".format(str(e)))
            self._close_connection()
            return False
        return True

    def _send_response(self):
        if self.client_connection is None:
            return False
        try:
            msg = 'A' * self.client_packet_size
            self.client_connection.sendall(str.encode(msg))
        except Exception as e:
            logger.log("TCP Server: Failed to send response to {}: {}".format(self.client_address, str(e)))
            return False
        finally:
            self._close_connection()
        return True

    def _close_connection(self):
        if self.client_connection is not None:
            self.client_connection.close()


class UDPServer(TransportServer):
    """
    UDP Server class
    """
    def __init__(self, ip, port, buffer_size):
        super().__init__(ip=ip, port=port, buffer_size=buffer_size)
        self.udp_server = None
        self.client_address = None
        self.client_packet_size = -1

    def _init(self):
        try:
            self.udp_server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.udp_server.bind((self.ip, self.port))
        except Exception as e:
            logger.log("UDP Server: Failed to init udp server: {}".format(str(e)))
            return False
        return True

    def _wait_for_data(self):
        try:
            # reset prev client address
            self.client_address = None
            data_from_client = self.udp_server.recvfrom(self.buffer_size)
            msg = data_from_client[0]
            self.client_address = data_from_client[1]
            self.client_packet_size = len(msg)
            logger.log("UDP Server: Get from client {} msg in size of {}".format(self.client_address, self.client_packet_size))
        except Exception as e:
            logger.log("UDP Server: Failed to receive data: {}".format(str(e)))
            return False
        return True

    def _send_response(self):
        if not self.client_address:
            return False
        try:
            msg = 'A' * self.client_packet_size
            self.udp_server.sendto(str.encode(msg), self.client_address)
        except Exception as e:
            logger.log("UDP Server: Failed to send response to {}: {}".format(self.client_address, str(e)))
            return False
        return True
