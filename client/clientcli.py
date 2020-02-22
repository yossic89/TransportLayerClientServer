import argparse

from client.src.clinet_runner import ClientRunner
from utilities import constants


def main():
    """
    cli method for running and testing client
    """
    # parse arg
    parser = argparse.ArgumentParser()

    parser.add_argument('-type', '--type', required=True, help="Select client type", choices=constants.SUPPORT_TYPES)
    parser.add_argument('-to', '--timeout', required=False, help="timeout for request, default in No timeout")
    parser.add_argument('-p', '--port', required=True, help="Connection port")
    parser.add_argument('-ps', '--packet_size', required=True, help="msg packet size")
    parser.add_argument('-ip', '--ip', required=True, help="server ip")

    args = parser.parse_args()
    ClientRunner(ip=args.ip, port=args.port, timeout=args.timeout, packet_size=args.packet_size, type=args.type).run()


if __name__ == "__main__":
    main()
