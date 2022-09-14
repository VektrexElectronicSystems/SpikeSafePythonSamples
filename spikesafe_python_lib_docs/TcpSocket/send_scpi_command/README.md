# spikesafe-python API Overview | TcpSocket | send_scpi_command(self, scpi_command, enable_logging = None)

## send_scpi_command(self, scpi_command, enable_logging = None)

### Definition
Sends a SCPI command via TCP/IP socket to a SpikeSafe.

### Parameters
scpi_command [string](https://docs.python.org/3/library/string.html)  
SCPI command to send to SpikeSafe

enable_logging [bool](https://docs.python.org/3/library/stdtypes.html#boolean-values) (Optional)  
Overrides spike_safe_socket.enable_logging attribute (None by default, will use spike_safe_socket.enable_logging value).

### Examples
The following example demonstrates the send_scpi_command function. It creates a new TcpSocket object, connects to a SpikeSafe, initiates the request for SpikeSafe information using the `*IDN?` SCPI command, reads the request response, and disconnects from a SpikeSafe.
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