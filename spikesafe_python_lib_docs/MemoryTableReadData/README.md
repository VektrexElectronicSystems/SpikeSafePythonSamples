# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [MemoryTableReadData](/spikesafe_python_lib_docs/MemoryTableReadData/README.md)

## MemoryTableReadData

### Definition
A class used to store data in a simple accessible object from a SpikeSafe's Memory Table Read response.

### Attributes
| Name | Description |
| - | - |
| [bulk_voltage](/spikesafe_python_lib_docs/MemoryTableReadData/bulk_voltage/README.md) | Bulk voltage (V) input to SpikeSafe. |
| [channel_data](/spikesafe_python_lib_docs/MemoryTableReadData/channel_data/README.md) | All channel data in list of ChannelData objects. Depending on the SpikeSafe model, a list may contain between 1 to 8 ChannelData objects. |
| [temperature_data](/spikesafe_python_lib_docs/MemoryTableReadData/temperature_data/README.md) | All temperature data in a list of TemperatureData objects. Depending on the SpikeSafe model, a list may contain between 1 to 4 TemperatureData objects. |

### Functions
| Name | Description |
| - | - |
| [bulk_voltage_volts_formatted_float(self)](/spikesafe_python_lib_docs/MemoryTableReadData/bulk_voltage_volts_formatted_float/README.md) | Return the bulk voltage reading formatted to matching hardware decimal places. |
| [bulk_voltage_volts_formatted_string(self)](/spikesafe_python_lib_docs/MemoryTableReadData/bulk_voltage_volts_formatted_string/README.md) | Return the bulk voltage reading formatted to matching hardware decimal places. |
| [parse_memory_table_read(self, get_memory_table_read_response)](/spikesafe_python_lib_docs/MemoryTableReadData/parse_memory_table_read/README.md) | Parses SpikeSafe's Memory Table Read response into a simple accessible object. |