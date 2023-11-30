# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Precision](/spikesafe_python_lib_docs/Precision/README.md) | get_precise_duty_cycle_command_argument(duty_cycle)

## get_precise_duty_cycle_command_argument(duty_cycle)

### Definition
Returns the optimal precision for a duty cycle command argument.

### Parameters
duty_cycle [float](https://docs.python.org/3/library/functions.html#float)  
Duty cycle to be sent to SpikeSafe
    
### Returns
[float](https://docs.python.org/3/library/functions.html#float)  
Duty cycle command argument with optimal precision

### Examples
The following example demonstrates the `get_precise_duty_cycle_command_argument()` function. It sends the SpikeSafe set current SCPI command with the optimum precision for 100mA.
```
# set Channel 1's current to 100 mA
tcp_socket.send_scpi_command(f'SOUR1:CURR {get_precise_current_command_argument(0.1)}')
```

### Examples In Action
[/run_spikesafe_operating_modes/run_dc/RunDcMode.py](/run_spikesafe_operating_modes/run_dc/RunDcMode.py)