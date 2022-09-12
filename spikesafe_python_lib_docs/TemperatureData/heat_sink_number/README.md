# spikesafe-python API Overview | MemoryTableReadData | heat_sink_number

## heat_sink_number

### Definition
Heat sink number

### Attribute Value
[int](https://docs.python.org/3/library/functions.html#int)  

### Examples
The following example demonstrates the heat_sink_number attribute. It initiates the request for SpikeSafe Memory Table Read and extracts bulk voltage, Channel 1's data, and Heat Sink 1's Temperature data from a MemoryTableReadData object.
```
# request SpikeSafe memory table
tcp_socket.send_scpi_command('MEM:TABL:READ')

# read SpikeSafe memory table
data = tcp_socket.read_data()                                        

# parse SpikeSafe memory table
memory_table_read = MemoryTableReadData().parse_memory_table_read(data)

# extract Bulk Voltage data
bulk_voltage = memory_table_read.bulk_voltage

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
[/getting_started/read_memory_table_data/ReadMemoryTableData.py](/getting_started/read_memory_table_data/ReadMemoryTableData.py)