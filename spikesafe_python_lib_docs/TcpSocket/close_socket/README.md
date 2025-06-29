# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md) | close_socket(self)

## close_socket(self)

### Definition
Closes TCP/IP socket used for remote communication to a SpikeSafe.

### Parameters
ip_address [string](https://docs.python.org/3/library/string.html)  
IP address of the SpikeSafe (10.0.0.220 to 10.0.0.0.251)

port_number [int](https://docs.python.org/3/library/functions.html#int)  
Port number of the SpikeSafe (8282 by default)

### Examples
The following example demonstrates the close_socket function. It creates a new TcpSocket object, connects to a SpikeSafe, initiates the request for SpikeSafe information using the `*IDN?` SCPI command, reads the request response, and disconnects from a SpikeSafe.
```
# instantiate new TcpSocket to connect to SpikeSafe
tcp_socket = TcpSocket(enable_logging=False)

# connect to SpikeSafe
tcp_socket.open_socket(ip_address, port_number)  

# request SpikeSafe information
tcp_socket.send_scpi_command('*IDN?')  
 
# read SpikeSafe information
data = tcp_socket.read_data()            

# disconnect from SpikeSafe
tcp_socket.close_socket() 
```

### Examples In Action
[/getting_started/read_idn/ReadIdnExpanded.py](/getting_started/read_idn/ReadIdnExpanded.py)