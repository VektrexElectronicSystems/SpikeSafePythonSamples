# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [MemoryTableReadData](/spikesafe_python_lib_docs/MemoryTableReadData/README.md) | bulk_voltage_volts_formatted_float(self)

## bulk_voltage_volts_formatted_float(self)

### Definition
Return the bulk voltage reading formatted to matching hardware decimal places.

### Returns
[float](https://docs.python.org/3/library/functions.html#float)  
Return the bulk voltage reading formatted to matching hardware decimal places.

### Examples
The following example demonstrates the bulk_voltage attribute. It initiates the request for SpikeSafe Memory Table Read and extracts bulk voltage, Channel 1's data, and Heat Sink 1's Temperature data from a MemoryTableReadData object.
```
# request SpikeSafe memory table
tcp_socket.send_scpi_command('MEM:TABL:READ')

# read SpikeSafe memory table
data = tcp_socket.read_data()                                        

# parse SpikeSafe memory table
memory_table_read = MemoryTableReadData().parse_memory_table_read(data)

# extract Bulk Voltage data
bulk_voltage = memory_table_read.bulk_voltage_volts_formatted_float()

# extract Channel 1's data
channel_number = memory_table_read.channel_data[0].channel_number
current_reading = memory_table_read.channel_data[0].current_reading
is_on_state = memory_table_read.channel_data[0].is_on_state
voltage_reading = memory_table_read.channel_data[0].voltage_reading

# extract Heatsink 1's Temperature Data
heat_sink_number = memory_table_read.temperature_data[0].heat_sink_number
temperature_reading = memory_table_read.temperature_data[0].temperature_reading
```

### Examples In Action