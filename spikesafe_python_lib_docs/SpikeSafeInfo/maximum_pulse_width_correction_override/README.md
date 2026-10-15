# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [SpikeSafeInfo](/spikesafe_python_lib_docs/SpikeSafeInfo/README.md) | maximum_pulse_width_correction_override

## maximum_pulse_width_correction_override

### Definition
Maximum pulse width correction override in microseconds.

### Attribute value
`float | None`. A newly constructed `SpikeSafeInfo` has `None` for this attribute.
[`SpikeSafeInfoParser.parse_spikesafe_info()`](/spikesafe_python_lib_docs/SpikeSafeInfoParser/parse_spikesafe_info/README.md)
populates it from the firmware version.

The parser sets this to `50` for Ethernet Processor firmware 3.0.15.5 or later,
and `9` for older firmware.

### Example
```python
import spikesafe_python

# tcp_socket is an open SpikeSafe TCP connection.
info = spikesafe_python.SpikeSafeInfoParser.parse_spikesafe_info(tcp_socket)
print(info.maximum_pulse_width_correction_override)
```
