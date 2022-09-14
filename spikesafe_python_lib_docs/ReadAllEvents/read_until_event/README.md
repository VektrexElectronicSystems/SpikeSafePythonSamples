# spikesafe-python API Overview | ReadAllEvents | read_until_event(spike_safe_socket, code, enable_logging = None)

## read_until_event(spike_safe_socket, code, enable_logging = None)

### Definition
Returns an array of all events from the SpikeSafe event queue until a specific event is read.

### Parameters
spike_safe_socket [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md)  
Socket object used to communicate with SpikeSafe.

code [int](https://docs.python.org/3/library/functions.html#int)  
Event code for desired event

enable_logging [bool](https://docs.python.org/3/library/stdtypes.html#boolean-values) (Optional)  
Overrides spike_safe_socket.enable_logging attribute (None by default, will use spike_safe_socket.enable_logging value).

### Returns
[EventData array](/spikesafe_python_lib_docs/EventData/README.md)  
All events from SpikeSafe leading to the desired event in a list of EventData objects.

### Examples
The following example demonstrates the read_until_event function. It setups up a SpikeSafe channel, starts it, waits until the event `100, Channel Ready` is returned from the SpikeSafe event queue, and monitors the event queue and readings once per second for 15 seconds.
```
# set Channel 1's pulse mode to DC and check for all events
tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP DC')    
log_all_events(tcp_socket)

# set Channel 1's safety threshold for over current protection to 50% and check for all events
tcp_socket.send_scpi_command('SOUR1:CURR:PROT 50')    
log_all_events(tcp_socket) 

# set Channel 1's current to 100 mA and check for all events
tcp_socket.send_scpi_command('SOUR1:CURR 0.01')        
log_all_events(tcp_socket)  

# set Channel 1's voltage to 10 V and check for all events
tcp_socket.send_scpi_command('SOUR1:VOLT 20')         
log_all_events(tcp_socket) 

# turn on Channel 1 and check for all events
tcp_socket.send_scpi_command('OUTP1 1')               
log_all_events(tcp_socket)                            

# wait until the channel is fully ramped to 10mA
read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

# check for all events and measure readings on Channel 1 once per second for 15 seconds,
# it is best practice to do this to ensure Channel 1 is on and does not have any errors
time_end = time.time() + 15                         
while time.time() < time_end:                       
    log_all_events(tcp_socket)
    log_memory_table_read(tcp_socket)
    wait(1)   
```

### Examples In Action
[/run_spikesafe_operating_modes/run_dc/RunDcMode.py](/run_spikesafe_operating_modes/run_dc/RunDcMode.py)