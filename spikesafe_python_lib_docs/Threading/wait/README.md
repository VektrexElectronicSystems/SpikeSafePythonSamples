# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Threading](/spikesafe_python_lib_docs/Threading/README.md) | wait(wait_time)

## wait(wait_time, current_time=time.perf_counter)

### Definition
Suspends the current thread for a specified amount of time.

### Parameters
wait_time [float](https://docs.python.org/3/library/functions.html#float)  
Wait time in seconds to suspend the current thread.

current_time [float](https://docs.python.org/3/library/functions.html#float)
Current time in seconds (time.perf_counter by default).

### Examples
The following example demonstrates the wait function. It setups up a SpikeSafe channel, starts it, waits until the event `100, Channel Ready` is returned from the SpikeSafe event queue, and monitors the event queue and readings once per second for 15 seconds.
```
# set Channel 1's pulse mode to DC and check for all events
tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP DC')    
log_all_events(tcp_socket)

# set Channel 1's safety threshold for over current protection to 50% and check for all events
tcp_socket.send_scpi_command('SOUR1:CURR:PROT 50')    
log_all_events(tcp_socket) 

# set Channel 1's current to 100 mA and check for all events
tcp_socket.send_scpi_command(f'SOUR1:CURR {get_precise_current_command_argument(0.1)}')         
log_all_events(tcp_socket)  

# set Channel 1's voltage to 10 V and check for all events
tcp_socket.send_scpi_command(f'SOUR1:VOLT {get_precise_compliance_voltage_command_argument(20)}')         
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