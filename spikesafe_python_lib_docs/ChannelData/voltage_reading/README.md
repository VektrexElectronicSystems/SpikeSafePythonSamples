# spikesafe-python API Overview | MemoryTableReadData | voltage_reading

## voltage_reading

### Definition
Channel voltage reading

### Attribute Value
[float](https://docs.python.org/3/library/functions.html#float)   

### Examples
The following example demonstrates the ChannelData attribute. It parses the SpikeSafe's Memory Table Read Response and extracts the Channel 1's ChannelData from a MemoryTableReadData object.
```
# request SpikeSafe memory table
tcp_socket.send_scpi_command('MEM:TABL:READ')

# read SpikeSafe memory table
data = tcp_socket.read_data()                                        

# parse SpikeSafe memory table
memory_table_read = MemoryTableReadData().parse_memory_table_read(data)

# extract Channel 1 data
channel_number = memory_table_read.channel_data[0].channel_number
current_reading = memory_table_read.channel_data[0].current_reading
is_on_state = memory_table_read.channel_data[0].is_on_state
voltage_reading = memory_table_read.channel_data[0].voltage_reading
```

### Examples In Action
[/getting_started/read_memory_table_data/ReadMemoryTableData.py](/getting_started/read_memory_table_data/ReadMemoryTableData.py)