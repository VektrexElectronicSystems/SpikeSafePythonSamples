# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Precision](/spikesafe_python_lib_docs/Precision/README.md) | Precision.get_precise_time_command_argument(time_seconds)

## Precision.get_precise_time_command_argument(time_seconds)

### Definition
Returns the optimal precision for a time in seconds command argument.

### Parameters
time_seconds [float](https://docs.python.org/3/library/functions.html#float)  
Time in seconds to be sent to SpikeSafe

### Returns
[string](https://docs.python.org/3/library/string.html)  
Time in seconds command argument with optimal precision

### Examples
The following example demonstrates the `spikesafe_python.Precision.get_precise_time_command_argument()` function. It sends the SpikeSafe pulse on time and pulse off time SCPI commands with the optimum precision for 1ms and 9ms.
```
# set Channel 1's Pulse On Time to 1ms and check for all events
tcp_socket.send_scpi_command(f'SOUR1:PULS:TON {spikesafe_python.Precision.get_precise_time_command_argument(0.001)}')

# set Channel 1's Pulse Off Time to 9ms and check for all events
tcp_socket.send_scpi_command(f'SOUR1:PULS:TOFF {spikesafe_python.Precision.get_precise_time_command_argument(0.009)}')
```

### Examples In Action
[/run_spikesafe_operating_modes/run_pulsed/RunPulsedMode.py](/run_spikesafe_operating_modes/run_pulsed/RunPulsedMode.py)