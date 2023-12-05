# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Compensation](/spikesafe_python_lib_docs/Compensation/README.md) | get_optimum_compensation(spikesafe_model_max_current_amps, set_current_amps)

## get_optimum_compensation(spikesafe_model_max_current_amps, set_current_amps)

### Definition
Returns the optimum compensation for a given set current.

### Parameters
spikesafe_model_max_current_amps [float](https://docs.python.org/3/library/functions.html#float)  
Maximum current of the SpikeSafe model

set_current_amps [float](https://docs.python.org/3/library/functions.html#float)  
Current to be set on SpikeSafe

### Returns
[int](https://docs.python.org/3/library/functions.html#int)  
Load impedance command argument with optimum compensation

[int](https://docs.python.org/3/library/functions.html#int)  
Rise time command argument with optimum compensation

### Raises
[ValueError](https://docs.python.org/3/library/exceptions.html#ValueError)  
If set_current_amps is greater than spikesafe_model_max_current_amps

### Examples
The following example demonstrates the `get_optimum_compensation()` function. It determines the optimum compensation settings to use based off the SpikeSafe's set current setting and maximum settable current.
```
# set Channel 1's current to 100 mA and check for all events
set_current = 0.1
tcp_socket.send_scpi_command(f'SOUR1:CURR {get_precise_current_command_argument(set_current)}')   
log_all_events(tcp_socket)  

# set Channel 1's compensation settings to their default values and check for all events
# For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
tcp_socket.send_scpi_command('SOUR1:CURR? MAX')
spikesafe_model_max_current = float(tcp_socket.read_data())
load_impedance, rise_time = get_optimum_compensation(spikesafe_model_max_current, set_current)
tcp_socket.send_scpi_command(f'SOUR1:PULS:CCOM {load_impedance}')
log_all_events(tcp_socket) 
tcp_socket.send_scpi_command(f'SOUR1:PULS:RCOM {rise_time}')
log_all_events(tcp_socket) 
```

### Examples In Action
[/run_spikesafe_operating_modes/run_pulsed/RunPulsedMode.py](/run_spikesafe_operating_modes/run_pulsed/RunPulsedMode.py)  
[/making_integrated_voltage_measurements/measure_voltage_across_pulse/MeasureVoltageAcrossPulse.py](/making_integrated_voltage_measurements/measure_voltage_across_pulse/MeasureVoltageAcrossPulse.py)