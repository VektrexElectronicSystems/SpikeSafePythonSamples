# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Discharge](/spikesafe_python_lib_docs/Discharge/README.md) | Discharge.get_spikesafe_channel_discharge_time(compliance_voltage)

## Discharge.get_spikesafe_channel_discharge_time(compliance_voltage)

### Definition
Returns the time in seconds to fully discharge the SpikeSafe channel based on the compliance voltage.

### Parameters
compliance_voltage [float](https://docs.python.org/3/library/functions.html#float)  
Compliance voltage to factor in discharge time

### Returns
[float](https://docs.python.org/3/library/functions.html#float)    
Discharge time in seconds

### Examples
The following example demonstrates the `spikesafe_python.Discharge.get_spikesafe_channel_discharge_time()` function. It checks for the time to fully discharge the SpikeSafe channel based on the compliance voltage, and waits for that period until restarting the channel.
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
spikesafe_python.Discharge.wait_for_spikesafe_channel_discharge(
    spikesafe_socket=tcp_socket, 
    spikesafe_info=spikesafe_info,
    compliance_voltage=compliance_voltage,
    channel_number=1)
```

### Examples In Action
[/getting_started/discharge_channel/discharge_channel.py](/getting_started/discharge_channel/discharge_channel.py)