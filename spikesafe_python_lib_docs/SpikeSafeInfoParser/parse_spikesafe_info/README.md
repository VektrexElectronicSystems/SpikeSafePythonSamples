# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [SpikeSafeInfoParser](/spikesafe_python_lib_docs/SpikeSafeInfoParser/README.md) | parse_spikesafe_info(spike_safe_socket, enable_logging = False)

## parse_spikesafe_info(spike_safe_socket, enable_logging = False)

### Definition
Parses the SpikeSafe information from the SCPI command responses.

### Parameters
spike_safe_socket [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md)  
Socket object used to communicate with SpikeSafe.

enable_logging [bool](https://docs.python.org/3/library/stdtypes.html#boolean-values) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Overrides spike_safe_socket.enable_logging attribute (None by default, will use spike_safe_socket.enable_logging value).

### Returns
[SpikeSafeInfo](/spikesafe_python_lib_docs/SpikeSafeInfo/README.md)  
An object containing the SpikeSafe information.

### Examples
The following example demonstrates the parse_spikesafe_info function. It connects to a SpikeSafe and calls the function which then returns an object with its information.
```
tcp_socket = spikesafe_python.TcpSocket()
tcp_socket.open_socket(ip_address, port_number)

tcp_socket.send_scpi_command('*RST') # "*RST" - reset to a known state (does not affect "VOLT" commands)
spikesafe_info = spikesafe_python.parse_spikesafe_info(tcp_socket) # parse the SpikeSafe information and print it to the log file

# log the SpikeSafe information. To access an attribute, use the dot operator (e.g. spikesafe_info.idn)
log.info(vars(spikesafe_info))

# log the information for each digitizer. To access an attribute, use the dot operator (e.g. digitizer.version)
for digitizer in spikesafe_info.digitizer_infos:
    log.info(vars(digitizer))
```

### Examples In Action
[/getting_started/read_idn/ReadSpikeSafeInfo.py](/getting_started/read_idn/ReadSpikeSafeInfo.py)