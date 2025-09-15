# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Compensation](/spikesafe_python_lib_docs/Compensation/README.md) | load_custom_compensation_table(file_path)

## load_custom_compensation_table(file_path)

### Definition
Returns a custom compensation table from a JSON file.

### Parameters
file_path [string](https://docs.python.org/3/library/string.html)  
Path to the JSON file containing the custom compensation table

### Returns
list [list([])](https://docs.python.org/3/library/stdtypes.html#list)  
Custom compensation table as a list of dictionaries conforming to the [custom_compensation_table_schema](/spikesafe_python_lib_docs/Compensation/custom_compensation_table_schema/README.md)  

### Raises
[FileNotFoundError](https://docs.python.org/3/library/exceptions.html#FileNotFoundError)  
If the file does not exist

[IOError](https://docs.python.org/3/library/exceptions.html#IOError)  
If an error occurs while loading the file

[ValueError](https://docs.python.org/3/library/exceptions.html#ValueError)  
If the file contains invalid JSON, schema validation error, or custom compensation table validation error

### Examples
The following example demonstrates the `load_custom_compensation_table()` function. It determines the custom compensation settings to use based off the SpikeSafe's set current setting, maximum settable current, and pulse on time.
```
# set Channel 1's Pulse On Time to 1ms and check for all events
pulse_on_time = 0.001
tcp_socket.send_scpi_command(f'SOUR1:PULS:TON {spikesafe_python.get_precise_time_command_argument(pulse_on_time)}')
spikesafe_python.log_all_events(tcp_socket) 

# set Channel 1's current to 100 mA and check for all events
set_current = 0.1
tcp_socket.send_scpi_command(f'SOUR1:CURR {spikesafe_python.get_precise_current_command_argument(set_current)}')   
spikesafe_python.log_all_events(tcp_socket)  

# set Channel 1's compensation settings to their default values and check for all events
# For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
tcp_socket.send_scpi_command('SOUR1:CURR? MAX')
spikesafe_model_max_current = float(tcp_socket.read_data())

# load custom_compensation_table from /test_compensation_files/valid.json
custom_compensation_table = spikesafe_python.load_custom_compensation_table(os.path.join(os.path.dirname(__file__), 'test_compensation_files', 'valid.json')
device_types = spikesafe_python.load_custom_compensation_unique_device_types(custom_compensation_table)
load_impedance, rise_time = spikesafe_python.get_custom_compensation(spikesafe_model_max_current, set_current, device_types[0], pulse_on_time)
tcp_socket.send_scpi_command(f'SOUR1:PULS:CCOM {load_impedance}')
spikesafe_python.log_all_events(tcp_socket) 
tcp_socket.send_scpi_command(f'SOUR1:PULS:RCOM {rise_time}')
spikesafe_python.log_all_events(tcp_socket) 
```

### Examples In Action