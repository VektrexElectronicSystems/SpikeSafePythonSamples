# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Compensation](/spikesafe_python_lib_docs/Compensation/README.md) | spikesafe_python.Compensation.get_optimum_compensation(spikesafe_model_max_current_amps, set_current_amps, pulse_on_time_seconds=None, enable_logging=False)

## spikesafe_python.Compensation.get_optimum_compensation(spikesafe_model_max_current_amps, set_current_amps, pulse_on_time_seconds=None, enable_logging=False)

### Definition
Returns the optimum compensation for a given set current, and optionally a given pulse on time.

### Parameters
spikesafe_model_max_current_amps [float](https://docs.python.org/3/library/functions.html#float)  
Maximum current of the SpikeSafe model

set_current_amps [float](https://docs.python.org/3/library/functions.html#float)  
Current to be set on SpikeSafe

pulse_on_time_seconds [float](https://docs.python.org/3/library/functions.html#float) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Pulse On Time to be set on SpikeSafe

enable_logging [bool](https://docs.python.org/3/library/stdtypes.html#boolean-values) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Enables logging (default is False)

### Returns
LoadImpedance [LoadImpedance](/spikesafe_python_lib_docs/SpikeSafeEnums/LoadImpedance/README.md)  
Load Impedance compensation value. This should be an instance of the LoadImpedance [IntEnum](https://docs.python.org/3/library/enum.html#enum.IntEnum) from SpikeSafeEnums
    
RiseTime [RiseTime](/spikesafe_python_lib_docs/SpikeSafeEnums/RiseTime/README.md)  
Rise Time compensation value. This should be an instance of the RiseTime [IntEnum](https://docs.python.org/3/library/enum.html#enum.IntEnum) from SpikeSafeEnums

### Raises
[ValueError](https://docs.python.org/3/library/exceptions.html#ValueError)  
If set_current_amps is greater than spikesafe_model_max_current_amps

### Remarks
This function assumes the set current is operating on the optimized current range. If operating on the high range with a set current normally programmed on the low range, the compensation values will not be optimal. See online specifications.
- [Source Measure Unit Precision Pulsed Current Performance Series Specifications](https://www.vektrex.com/downloads/vektrex-spikesafe-smu-specifications.pdf)
- [High Current Performance Series Precision Pulsed Current Source Measure Unit Specifications](https://www.vektrex.com/downloads/High-Current-SpikeSafe-Performance-Series-Precision-Pulsed-Source-Measure-Unit-Specifications.pdf)
- [SpikeSafe™ Performance Series Precision Pulsed Current Source Specifications](https://www.vektrex.com/downloads/vektrex-spikesafe-performance-series-precision-pulsed-current-source-specifications.pdf)

If Load Impedance is returned as Medium or High, it is best practice to increase the Compliance Voltage setting by 5V to 30V. This helps the current amplifier to overcome inductance. If Compliance Voltage is not increased, then a Low Side Over Current or an Unstable Waveform error may occur.

If an Operating Mode is used to sweep through steps of currents where the compensation settings are the same across the sweep, such as Pulse Sweep or Multiple Pulse Burst, it is recommended use the optimum compensation settings targeting the Stop Current.

### Examples
The following example demonstrates the `spikesafe_python.Compensation.get_optimum_compensation()` function. It determines the optimum compensation settings to use based off the SpikeSafe's set current setting, maximum settable current, and pulse on time.
```
# set Channel 1's Pulse On Time to 1ms and check for all events
pulse_on_time = 0.001
tcp_socket.send_scpi_command(f'SOUR1:PULS:TON {spikesafe_python.Precision.get_precise_time_command_argument(pulse_on_time)}')
spikesafe_python.ReadAllEvents.log_all_events(tcp_socket) 

# set Channel 1's current to 100 mA and check for all events
set_current = 0.1
tcp_socket.send_scpi_command(f'SOUR1:CURR {spikesafe_python.Precision.get_precise_current_command_argument(set_current)}')   
spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)  

# set Channel 1's compensation settings to their default values and check for all events
# For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
tcp_socket.send_scpi_command('SOUR1:CURR? MAX')
spikesafe_model_max_current = float(tcp_socket.read_data())
load_impedance, rise_time = spikesafe_python.Compensation.get_optimum_compensation(spikesafe_model_max_current, set_current, pulse_on_time)
tcp_socket.send_scpi_command(f'SOUR1:PULS:CCOM {load_impedance}')
spikesafe_python.ReadAllEvents.log_all_events(tcp_socket) 
tcp_socket.send_scpi_command(f'SOUR1:PULS:RCOM {rise_time}')
spikesafe_python.ReadAllEvents.log_all_events(tcp_socket) 
```

### Examples In Action
[/run_spikesafe_operating_modes/run_pulsed/RunPulsedMode.py](/run_spikesafe_operating_modes/run_pulsed/RunPulsedMode.py)  
[/making_integrated_voltage_measurements/measure_voltage_across_pulse/MeasureVoltageAcrossPulse.py](/making_integrated_voltage_measurements/measure_voltage_across_pulse/MeasureVoltageAcrossPulse.py)