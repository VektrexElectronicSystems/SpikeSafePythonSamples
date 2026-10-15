# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [TemperatureData](/spikesafe_python_lib_docs/TemperatureData/README.md) | parse_temperature_data

## parse_temperature_data(temperature_memory_table_read_response: str) -> TemperatureData

### Definition
Parses one heat-sink temperature portion of a memory-table response into the current object. Numeric fields use a period decimal separator.

### Parameters
`temperature_memory_table_read_response` (`str`): the parenthesized response portion, such as `"(T1 20.7)"`.

### Returns
The same `TemperatureData` instance with parsed attributes. Parsing errors are logged and
re-raised; the object may be partially updated if parsing fails.

### Example
```python
import spikesafe_python

data = spikesafe_python.TemperatureData().parse_temperature_data("(T1 20.7)")
```
