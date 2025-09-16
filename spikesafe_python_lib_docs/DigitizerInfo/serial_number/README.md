# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerInfo](/spikesafe_python_lib_docs/DigitizerInfo/README.md) | serial_number

## serial_number

### Definition
Digitizer serial number

### Attribute Value
[string](https://docs.python.org/3/library/string.html)  

### Examples
The following example demonstrates the parse_spikesafe_info function. It connects to a SpikeSafe and calls the function which then returns an object with its information.
```
tcp_socket = spikesafe_python.TcpSocket()
tcp_socket.open_socket(ip_address, port_number)

tcp_socket.send_scpi_command('*RST') # "*RST" - reset to a known state (does not affect "VOLT" commands)
spikesafe_info = spikesafe_python.SpikeSafeInfoParser.parse_spikesafe_info(tcp_socket) # parse the SpikeSafe information and print it to the log file

# log the SpikeSafe information. To access an attribute, use the dot operator (e.g. spikesafe_info.idn)
log.info(vars(spikesafe_info))

# log the information for each digitizer. To access an attribute, use the dot operator (e.g. digitizer.version)
for digitizer in spikesafe_info.digitizer_infos:
    log.info(vars(digitizer))
```

### Examples In Action
[/getting_started/read_idn/ReadSpikeSafeInfo.py](/getting_started/read_idn/ReadSpikeSafeInfo.py)