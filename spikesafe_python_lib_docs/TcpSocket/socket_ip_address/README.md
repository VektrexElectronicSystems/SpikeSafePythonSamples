# spikesafe-python API Overview | TcpSocket | socket_ip_address

## socket_ip_address

### Definition
IP address of for the TCP/IP socket.

### Attribute Value
[string](https://docs.python.org/3/library/string.html)  

### Examples
The following example demonstrates the socket_ip_address attribute. It creates a new TcpSocket object, connects to a SpikeSafe, and logs its IP address to a file.
```
# instantiate new TcpSocket to connect to SpikeSafe
tcp_socket = TcpSocket()

# connect to SpikeSafe
tcp_socket.open_socket(ip_address, port_number)  
log.info(tcp_socket.socket_ip_address)
```

[/getting_started/tcp_socket_sample/TcpSample.py](/getting_started/tcp_socket_sample/TcpSample.py)