# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [ChannelData](/spikesafe_python_lib_docs/ChannelData/README.md) | parse_channel_data

## parse_channel_data(channel_memory_table_read_response: str) -> ChannelData

### Definition
Parses one channel portion of a memory-table response into the current object. Numeric fields use a period decimal separator.

### Parameters
`channel_memory_table_read_response` (`str`): the parenthesized response portion, such as `"(CH1 10.123456 1.123000 1)"`.

### Returns
The same `ChannelData` instance with parsed attributes. Parsing errors are logged and
re-raised; the object may be partially updated if parsing fails.

### Example
```python
import spikesafe_python

data = spikesafe_python.ChannelData().parse_channel_data("(CH1 10.123456 1.123000 1)")
```
