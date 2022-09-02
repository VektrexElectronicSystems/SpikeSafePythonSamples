# spikesafe-python API Overview | TcpSocket | tcp_socket

## tcp_socket

### Definition
TCP/IP socket for remote communication to a SpikeSafe.

### Attribute Value
[socket](https://docs.python.org/3/library/socket.html)  
A new socket object.

### Examples
The following example demonstrates the socket attribute. It creates a new socket object to connect to a host with streaming communication, with a 2 second time out, and then connects the socket to a SpikeSafe at remote address of 10.0.0.220 on port 8282.
```
# create socket object
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2 second socket timeout
tcp_socket.settimeout(2)                                        

# connect to SpikeSafe
tcp_socket.connect('10.0.0.220', 8282)
```

### Examples In Action
[/getting_started/tcp_socket_sample/TcpSample.py](/getting_started/tcp_socket_sample/TcpSample.py)