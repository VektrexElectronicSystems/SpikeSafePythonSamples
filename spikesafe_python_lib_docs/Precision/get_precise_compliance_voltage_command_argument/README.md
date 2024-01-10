# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Precision](/spikesafe_python_lib_docs/Precision/README.md) | get_precise_compliance_voltage_command_argument(compliance_voltage)

## get_precise_compliance_voltage_command_argument(compliance_voltage)

### Definition
Returns the optimal precision for a compliance voltage command argument.

### Parameters
compliance_voltage [float](https://docs.python.org/3/library/functions.html#float)  
Compliance voltage to be sent to SpikeSafe
    
### Returns
[float](https://docs.python.org/3/library/functions.html#float)  
Compliance voltage command argument with optimal precision

### Examples
The following example demonstrates the `get_precise_compliance_voltage_command_argument()` function. It sends the SpikeSafe compliance voltage SCPI command with the optimum precision for 20V.
```
# set Channel 1's voltage to 10 V and check for all events
tcp_socket.send_scpi_command(f'SOUR1:VOLT {get_precise_compliance_voltage_command_argument(20)}') 
```

### Examples In Action
[/run_spikesafe_operating_modes/run_dc/RunDcMode.py](/run_spikesafe_operating_modes/run_dc/RunDcMode.py)