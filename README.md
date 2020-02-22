# TransportLayerClientServer
## Components
### Server - can run tcp or/and udp(can run in parallel) server for ip and port
### Client - one time client for tcp or udp cleint for server ip, port and packet size

## How To Run(cli mode)
### Server
* run server/servercli.py
* with the next argumets:
  *   -h, --help            show this help message and exit
  *   -tcp, --tcp           Run tcp server
  *   -udp, --udp           Run udp server
  *   -p , --port   Binding port
  *   -bs BUFFER_SIZE, --buffer_size  max buffer size support
  *   -ip , --ip       local ip to bind

### Client
* run client/clientcli.py
* with the next argumets:
**    -h, --help            show this help message and exit
**    -type {tcp,udp}, --type {tcp,udp} Select client type
**    -to , --timeout timeout for request, default in No timeout
**    -p , --port  Connection port
**    -ps , --packet_size   msg packet size
**    -ip , --ip server ip
