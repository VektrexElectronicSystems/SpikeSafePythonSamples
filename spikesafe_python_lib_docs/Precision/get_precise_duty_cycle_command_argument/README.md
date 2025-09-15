# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Precision](/spikesafe_python_lib_docs/Precision/README.md) | spikesafe_python.get_precise_duty_cycle_command_argument(duty_cycle)

## spikesafe_python.get_precise_duty_cycle_command_argument(duty_cycle)

### Definition
Returns the optimal precision for a duty cycle command argument.

### Parameters
duty_cycle [float](https://docs.python.org/3/library/functions.html#float)  
Duty cycle to be sent to SpikeSafe
    
### Returns
[string](https://docs.python.org/3/library/string.html)  
Duty cycle command argument with optimal precision

### Examples
The following example demonstrates the `spikesafe_python.get_precise_duty_cycle_command_argument()` function. It sends the SpikeSafe duty cycle SCPI command with the optimum precision for 50%.
```
# set Channel 1's Duty Cycle to 50%.
tcp_socket.send_scpi_command(f'SOUR1:PULS:DCYC {spikesafe_python.get_precise_duty_cycle_command_argument(50)}')
```

### Examples In Action
[/application_specific_examples/using_pulse_holds/UsingPulseHolds.py](/application_specific_examples/using_pulse_holds/UsingPulseHolds.py)