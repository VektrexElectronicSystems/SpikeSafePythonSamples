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

### Examples In Action