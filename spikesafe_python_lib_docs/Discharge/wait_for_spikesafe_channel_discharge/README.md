# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Discharge](/spikesafe_python_lib_docs/Discharge/README.md) | Discharge.wait_for_spikesafe_channel_discharge(spike_safe_socket: TcpSocket, spikesafe_info: SpikeSafeInfo, compliance_voltage: float, channel_number: int = 1, enable_logging: bool | None = None) -> None

## Discharge.wait_for_spikesafe_channel_discharge(spike_safe_socket: TcpSocket, spikesafe_info: SpikeSafeInfo, compliance_voltage: float, channel_number: int = 1, enable_logging: bool | None = None) -> None

### Definition
Automatically waits for the SpikeSafe channel to fully discharge based on SpikeSafe capabilities.
If the SpikeSafe supports the Discharge Complete query, it will poll the channel until discharge is complete.
If not, it will wait for a calculated time based on the compliance voltage.

### Parameters
spike_safe_socket [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md)  
Socket object used to communicate with SpikeSafe.

spikesafe_info [SpikeSafeInfo](/spikesafe_python_lib_docs/SpikeSafeInfo/README.md)  
An object containing the SpikeSafe information.

compliance_voltage [float](https://docs.python.org/3/library/functions.html#float)  
Compliance voltage to factor in discharge time.

channel_number [int](https://docs.python.org/3/library/functions.html#int)  
Channel number to wait for discharge. By default, this is 1.

enable_logging [bool](https://docs.python.org/3/library/stdtypes.html#boolean-values) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Overrides spike_safe_socket.enable_logging attribute (None by default, will use spike_safe_socket.enable_logging value).

### Examples
The following example demonstrates the `spikesafe_python.Discharge.wait_for_spikesafe_channel_discharge()` function. After the SpikeSafe Channel is turned off, the channel is fully discharged.
```
# parse the SpikeSafe information
spikesafe_info = spikesafe_python.SpikeSafeInfoParser.parse_spikesafe_info(tcp_socket)

# start test #1 by turning on Channel 1 and check for all events
tcp_socket.send_scpi_command('OUTP1 1')               
spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

# wait until the channel is fully ramped to 10mA
spikesafe_python.ReadAllEvents.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

# check for all events and measure readings on Channel 1 once per second for 5 seconds,
# it is best practice to do this to ensure Channel 1 is on and does not have any errors
time_end = time.time() + 5                         
while time.time() < time_end:                       
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)
    spikesafe_python.MemoryTableReadData.log_memory_table_read(tcp_socket)
    spikesafe_python.Threading.wait(1)    

# turn off Channel 1 and check for all events
tcp_socket.send_scpi_command('OUTP1 0', enable_logging=True)               
spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

# wait until the channel is fully discharged before starting test #2
log.info('Waiting for Channel 1 to fully discharge after test #1...')
if spikesafe_info.supports_discharge_query:
    spikesafe_python.Discharge.wait_for_spikesafe_channel_discharge(
        spikesafe_socket: tcp_socket, 
        spikesafe_info: spikesafe_info,
        compliance_voltage: compliance_voltage,
        channel_number=1, 
        enable_logging=True)
else:
    wait_time = spikesafe_python.Discharge.get_spikesafe_channel_discharge_time(compliance_voltage)
    spikesafe_python.Threading.wait(wait_time)
```

### Examples In Action
[/getting_started/discharge_channel/discharge_channel.py](/getting_started/discharge_channel/discharge_channel.py)