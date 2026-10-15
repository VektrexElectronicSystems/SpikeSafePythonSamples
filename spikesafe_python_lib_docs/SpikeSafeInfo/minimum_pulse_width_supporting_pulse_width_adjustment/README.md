# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [SpikeSafeInfo](/spikesafe_python_lib_docs/SpikeSafeInfo/README.md) | minimum_pulse_width_supporting_pulse_width_adjustment

## minimum_pulse_width_supporting_pulse_width_adjustment

### Definition
Minimum pulse width supporting pulse width adjustment, in seconds.

### Attribute value
`float | None`. A newly constructed `SpikeSafeInfo` has `None` for this attribute.
[`SpikeSafeInfoParser.parse_spikesafe_info()`](/spikesafe_python_lib_docs/SpikeSafeInfoParser/parse_spikesafe_info/README.md)
populates it from the firmware version.

The parser sets this to `0.000005` (5 microseconds) for Ethernet Processor firmware
3.0.18.1 or later, and `0.00001` (10 microseconds) for older firmware.

### Example
```python
import spikesafe_python

# tcp_socket is an open SpikeSafe TCP connection.
info = spikesafe_python.SpikeSafeInfoParser.parse_spikesafe_info(tcp_socket)
print(info.minimum_pulse_width_supporting_pulse_width_adjustment)
```
