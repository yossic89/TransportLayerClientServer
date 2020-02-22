from server.src.transport_server import UDPServer, TCPServer
from utilities.logger import Logger
import threading
logger = Logger.instance()


class ServerRunner(object):
    """
    runner for server
    can run TCP and udp server in parallel for the same port
    """
    def __init__(self, ip, port, buffer_size, run_tcp, run_udp):
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.run_tcp = run_tcp
        self.run_udp = run_udp

    def run(self):
        server_threads = []
        if self.run_udp:
            udp_server = UDPServer(ip=self.ip, port=self.port, buffer_size=self.buffer_size)
            server_threads.append(threading.Thread(target=udp_server.run_server))

        if self.run_tcp:
            tcp_server = TCPServer(ip=self.ip, port=self.port, buffer_size=self.buffer_size)
            server_threads.append(threading.Thread(target=tcp_server.run_server))

        for t in server_threads:
            t.start()
        for t in server_threads:
            t.join()
