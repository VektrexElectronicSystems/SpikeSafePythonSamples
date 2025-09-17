# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [ScpiFormatter](/spikesafe_python_lib_docs/ScpiFormatter/README.md) | get_scpi_format_on_state_for_bool

## get_scpi_format_on_state_for_bool

### Definition
Return the SCPI formatted value for a boolean value

### Returns
[string](https://docs.python.org/3/library/string.html)  
Return the SCPI formatted value for a boolean value. 'ON' for True, 'OFF' for False.

### Examples
The following example demonstrates the `get_scpi_format_on_state_for_bool()` function. It sends the SpikeSafe PSMU pulse width adjustment SCPI command.
```
# set the SpikeSafe Pulse Width Adjustment to on
pulse_width_adjustment = True
tcp_socket.send_scpi_command(f'SOUR1:PULS:AADJ {spikesafe_python.ScpiFormatter.get_scpi_format_on_state_for_bool(pulse_width_adjustment)}') 

```

### Examples In Action