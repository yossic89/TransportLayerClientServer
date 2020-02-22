import argparse

from server.src.server_runner import ServerRunner


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-tcp', '--tcp', action='store_true', help="Run tcp server")
    parser.add_argument('-udp', '--udp', action='store_true', help="Run udp server")
    parser.add_argument('-p', '--port', required=True, help="Binding port")
    parser.add_argument('-bs', '--buffer_size', required=True, help="max buffer size support")
    parser.add_argument('-ip', '--ip', required=True, help="local ip to bind")

    args = parser.parse_args()
    ServerRunner(ip=args.ip, port=args.port, buffer_size=args.buffer_size, run_tcp=args.tcp, run_udp=args.udp).run()


if __name__ == "__main__":
    main()
