# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Precision](/spikesafe_python_lib_docs/Precision/README.md) | spikesafe_python.get_precise_time_microseconds_command_argument(time_microseconds)

## spikesafe_python.get_precise_time_microseconds_command_argument(time_microseconds)

### Definition
Returns the optimal precision for a time in microseconds command argument.

### Parameters
time_microseconds [float](https://docs.python.org/3/library/functions.html#float)  
Time in microseconds to be sent to SpikeSafe

### Returns
[string](https://docs.python.org/3/library/string.html)  
Time in microseconds command argument with optimal precision

### Examples
The following example demonstrates the `spikesafe_python.get_precise_time_microseconds_command_argument()` function. It sends the SpikeSafe PSMU Digitizer aperture and hardware trigger delay SCPI commands with the optimum precision for 600us and 200us.
```
# set Digitizer aperture for 600µs. Aperture specifies the measurement time, and we want to measure a majority of the pulse's constant current output
aperture = 600
tcp_socket.send_scpi_command(f'VOLT:APER {spikesafe_python.get_precise_time_microseconds_command_argument(aperture)}')

# set Digitizer trigger delay to 200µs. We want to give sufficient delay to omit any overshoot the current pulse may have
hardware_trigger_delay = 200
tcp_socket.send_scpi_command(f'VOLT:TRIG:DEL {spikesafe_python.get_precise_time_microseconds_command_argument(hardware_trigger_delay)}')
```

### Examples In Action
[/making_integrated_voltage_measurements/measure_all_pulsed_voltages/README.md](/making_integrated_voltage_measurements/measure_all_pulsed_voltages/README.md)