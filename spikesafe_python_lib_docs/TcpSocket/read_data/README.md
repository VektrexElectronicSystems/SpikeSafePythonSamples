# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md) | read_data(self, enable_logging = None)

## read_data(self, enable_logging = None)

### Definition
Reads data reply via TCP/IP socket from a SpikeSafe.

### Parameters
enable_logging [bool](https://docs.python.org/3/library/stdtypes.html#boolean-values) (Optional)  
Overrides spike_safe_socket.enable_logging attribute (None by default, will use spike_safe_socket.enable_logging value).

### Returns
[string](https://docs.python.org/3/library/string.html)  
A string that represents the data reply from a SpikeSafe.

### Examples
The following example demonstrates the read_data function. It creates a new TcpSocket object, connects to a SpikeSafe, initiates the request for SpikeSafe information using the `*IDN?` SCPI command, reads the request response, and disconnects from a SpikeSafe.
```
# instantiate new TcpSocket to connect to SpikeSafe
tcp_socket = TcpSocket()

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