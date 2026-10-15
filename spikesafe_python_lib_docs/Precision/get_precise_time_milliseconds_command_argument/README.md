# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Precision](/spikesafe_python_lib_docs/Precision/README.md) | get_precise_time_milliseconds_command_argument

## Precision.get_precise_time_milliseconds_command_argument(time_milliseconds: float) -> str

### Definition
Formats a time in milliseconds using three decimal places. The decimal separator
is always a period, with no digit grouping, regardless of locale.

### Parameters
`time_milliseconds` (`float`): time in milliseconds. No unit conversion is performed.

### Returns
`str`: the time with three decimal places. Use only with commands that expect
milliseconds; commands expecting seconds or microseconds need the corresponding helper.

### Example
```python
import spikesafe_python

argument = spikesafe_python.Precision.get_precise_time_milliseconds_command_argument(1.25)
assert argument == "1.250"
```
