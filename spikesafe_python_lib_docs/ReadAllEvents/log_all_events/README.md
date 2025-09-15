# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [ReadAllEvents](/spikesafe_python_lib_docs/ReadAllEvents/README.md) | spikesafe_python.log_all_events(spike_safe_socket)

## spikesafe_python.log_all_events(spike_safe_socket)

### Definition
Reads all SpikeSafe events from event queue and prints them to the log file.

### Parameters
spike_safe_socket [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md)  
Socket object used to communicate with SpikeSafe.

### Examples
The following example demonstrates the spikesafe_python.log_all_events function. It setups up a SpikeSafe channel, starts it, waits until the event `100, Channel Ready` is returned from the SpikeSafe event queue, and monitors the event queue and readings once per second for 15 seconds.
```
# set Channel 1's pulse mode to DC and check for all events
tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP DC')    
spikesafe_python.log_all_events(tcp_socket)

# set Channel 1's safety threshold for over current protection to 50% and check for all events
tcp_socket.send_scpi_command('SOUR1:CURR:PROT 50')    
spikesafe_python.log_all_events(tcp_socket) 

# set Channel 1's current to 100 mA and check for all events
tcp_socket.send_scpi_command(f'SOUR1:CURR {spikesafe_python.get_precise_current_command_argument(0.1)}')         
spikesafe_python.log_all_events(tcp_socket)  

# set Channel 1's voltage to 10 V and check for all events
tcp_socket.send_scpi_command(f'SOUR1:VOLT {spikesafe_python.get_precise_compliance_voltage_command_argument(20)}')         
spikesafe_python.log_all_events(tcp_socket) 

# turn on Channel 1 and check for all events
tcp_socket.send_scpi_command('OUTP1 1')               
spikesafe_python.log_all_events(tcp_socket)                            

# wait until the channel is fully ramped to 10mA
spikesafe_python.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

# check for all events and measure readings on Channel 1 once per second for 15 seconds,
# it is best practice to do this to ensure Channel 1 is on and does not have any errors
time_end = time.time() + 15                         
while time.time() < time_end:                       
    spikesafe_python.log_all_events(tcp_socket)
    spikesafe_python.log_memory_table_read(tcp_socket)
    spikesafe_python.wait(1)   
```

### Examples In Action
[/run_spikesafe_operating_modes/run_dc/RunDcMode.py](/run_spikesafe_operating_modes/run_dc/RunDcMode.py)