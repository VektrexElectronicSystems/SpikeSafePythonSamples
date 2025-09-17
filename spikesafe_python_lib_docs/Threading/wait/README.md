# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Threading](/spikesafe_python_lib_docs/Threading/README.md) | Threading.wait(wait_time, os_timer_resolution_offset_time=0, current_time=time.perf_counter)

## Threading.wait(wait_time, os_timer_resolution_offset_time=0, current_time=time.perf_counter)

### Definition
Suspends the current thread for a specified amount of time.

### Parameters
wait_time [float](https://docs.python.org/3/library/functions.html#float)  
Wait time in seconds to suspend the current thread.

os_timer_resolution_offset_time [float](https://docs.python.org/3/library/functions.html#float) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
The offset time in seconds to add to wait_time due to the operating system timer resolution limit. Default is 0.

current_time [float](https://docs.python.org/3/library/functions.html#float) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)    
Current time in seconds (time.perf_counter by default).

### Remarks
The resolution of system timers between operating systems refers to the precision with which a system can measure and manage time. Different operating systems may have varying timer resolutions, which can impact tasks like scheduling, synchronization, and overall system performance.

Windows operating systems use the concept of a system timer tick, whose default timer resolution is typically in the range of 10 milliseconds to 16 milliseconds (see [GetTickCount64 function](https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-gettickcount64)).

macOS is similar to Linux (see [mach_absolute_time function](https://developer.apple.com/documentation/kernel/1462446-mach_absolute_time)).

Linux operating systems use the kernel based High-Resolution Timer (HRT) framework to provide more accurate timing, whose default timer resolution can be as low as 1 nanosecond in recent Linux kernels (see [hrtimers - subsystem for high-resolution kernel timers](https://docs.kernel.org/timers/hrtimers.html) and [High Resolution Timers](https://elinux.org/High_Resolution_Timers#:~:text=Currently%2C%20timers%20in%20Linux%20are,milliseconds%20on%20most%20embedded%20platforms.)).

### Examples
The following example demonstrates the wait function. It setups up a SpikeSafe channel, starts it, waits until the event `100, Channel Ready` is returned from the SpikeSafe event queue, and monitors the event queue and readings once per second for 15 seconds.
```
# set Channel 1's pulse mode to DC and check for all events
tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP DC')    
spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

# set Channel 1's safety threshold for over current protection to 50% and check for all events
tcp_socket.send_scpi_command('SOUR1:CURR:PROT 50')    
spikesafe_python.ReadAllEvents.log_all_events(tcp_socket) 

# set Channel 1's current to 100 mA and check for all events
tcp_socket.send_scpi_command(f'SOUR1:CURR {spikesafe_python.Precision.get_precise_current_command_argument(0.1)}')         
spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)  

# set Channel 1's voltage to 10 V and check for all events
tcp_socket.send_scpi_command(f'SOUR1:VOLT {spikesafe_python.Precision.get_precise_compliance_voltage_command_argument(20)}')         
spikesafe_python.ReadAllEvents.log_all_events(tcp_socket) 

# turn on Channel 1 and check for all events
tcp_socket.send_scpi_command('OUTP1 1')               
spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)                            

# wait until the channel is fully ramped to 10mA
spikesafe_python.ReadAllEvents.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

# check for all events and measure readings on Channel 1 once per second for 15 seconds,
# it is best practice to do this to ensure Channel 1 is on and does not have any errors
time_end = time.time() + 15                         
while time.time() < time_end:                       
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)
    spikesafe_python.MemoryTableReadData.log_memory_table_read(tcp_socket)
    spikesafe_python.Threading.wait(1)   
```

### Examples In Action
[/run_spikesafe_operating_modes/run_dc/RunDcMode.py](/run_spikesafe_operating_modes/run_dc/RunDcMode.py)