# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Compensation](/spikesafe_python_lib_docs/Compensation/README.md) | get_custom_compensation(spikesafe_model_max_current_amps, set_current_amps, device_type, custom_compensation_table, pulse_on_time_seconds=None, enable_logging=True)

## get_custom_compensation(spikesafe_model_max_current_amps, set_current_amps, device_type, custom_compensation_table, pulse_on_time_seconds=None, enable_logging=True)

### Definition
Returns the custom compensation values for a given set_current_amps and device_type based on a custom_compensation_table, and optionally a given pulse on time.

### Parameters
spikesafe_model_max_current_amps [float](https://docs.python.org/3/library/functions.html#float)  
Maximum current of the SpikeSafe model

set_current_amps [float](https://docs.python.org/3/library/functions.html#float)  
Current to be set on SpikeSafe

device_type [string](https://docs.python.org/3/library/string.html)  
Device type of the DUT

custom_compensation_table [list([])](https://docs.python.org/3/library/stdtypes.html#list)  
Custom compensation table to be used for compensation. This should be the result of calling the [load_custom_compensation_table(file_path)](/spikesafe_python_lib_docs/Compensation/load_custom_compensation_table/README.md) function conforming to the [custom_compensation_table_schema](/spikesafe_python_lib_docs/Compensation/custom_compensation_table_schema/README.md)  

pulse_on_time_seconds [float](https://docs.python.org/3/library/functions.html#float) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Pulse On Time to be set on SpikeSafe

enable_logging [bool](https://docs.python.org/3/library/stdtypes.html#boolean-values) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Enables logging (default is True)

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

If an Operating Mode is used to sweep through steps of currents where the compensation settings are the same across the sweep, such as Pulse Sweep or Multiple Pulse Burst, it is recommended use the custom compensation settings targeting the Stop Current.

### Examples
The following example demonstrates the `get_custom_compensation()` function. It determines the custom compensation settings to use based off the SpikeSafe's set current setting, maximum settable current, and pulse on time.
```
# set Channel 1's Pulse On Time to 1ms and check for all events
pulse_on_time = 0.001
tcp_socket.send_scpi_command(f'SOUR1:PULS:TON {get_precise_time_command_argument(pulse_on_time)}')
log_all_events(tcp_socket) 

# set Channel 1's current to 100 mA and check for all events
set_current = 0.1
tcp_socket.send_scpi_command(f'SOUR1:CURR {get_precise_current_command_argument(set_current)}')   
log_all_events(tcp_socket)  

# set Channel 1's compensation settings to their default values and check for all events
# For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
tcp_socket.send_scpi_command('SOUR1:CURR? MAX')
spikesafe_model_max_current = float(tcp_socket.read_data())

# load custom_compensation_table from /test_compensation_files/valid.json
custom_compensation_table = load_custom_compensation_table(os.path.join(os.path.dirname(__file__), 'test_compensation_files', 'valid.json')
device_types = load_custom_compensation_unique_device_types(custom_compensation_table)
load_impedance, rise_time = get_custom_compensation(spikesafe_model_max_current, set_current, device_types[0], pulse_on_time)
tcp_socket.send_scpi_command(f'SOUR1:PULS:CCOM {load_impedance}')
log_all_events(tcp_socket) 
tcp_socket.send_scpi_command(f'SOUR1:PULS:RCOM {rise_time}')
log_all_events(tcp_socket) 
```

### Examples In Action