# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Precision](/spikesafe_python_lib_docs/Precision/README.md) | Precision.get_precise_current_command_argument(current_amps)

## Precision.get_precise_current_command_argument(current_amps)

### Definition
Returns the optimal precision for a current in amps command argument.

### Parameters
current_amps [float](https://docs.python.org/3/library/functions.html#float)  
Current in amps to be sent to SpikeSafe
    
### Returns
[string](https://docs.python.org/3/library/string.html)  
Current in amps command argument with optimal precision

### Examples
The following example demonstrates the `spikesafe_python.Precision.get_precise_current_command_argument()` function. It sends the SpikeSafe set current SCPI command with the optimum precision for 100mA.
```
# set Channel 1's current to 100 mA
tcp_socket.send_scpi_command(f'SOUR1:CURR {spikesafe_python.Precision.get_precise_current_command_argument(0.1)}')
```

### Examples In Action
[/run_spikesafe_operating_modes/run_dc/RunDcMode.py](/run_spikesafe_operating_modes/run_dc/RunDcMode.py)