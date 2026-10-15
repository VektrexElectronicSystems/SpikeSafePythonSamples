# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [PulseWidthCorrection](/spikesafe_python_lib_docs/PulseWidthCorrection/README.md) | get_optimum_pulse_width_correction

## PulseWidthCorrection.get_optimum_pulse_width_correction(spikesafe_info, set_current_amps, load_impedance, rise_time)

### Definition
Calculates a correction using the model's compensation table and current range.
The calculation assumes the instrument is operating on the optimized current range.

### Parameters
| Name | Type | Description |
| - | - | - |
| spikesafe_info | [SpikeSafeInfo](/spikesafe_python_lib_docs/SpikeSafeInfo/README.md) | Parsed instrument information, including maximum current and correction override. |
| set_current_amps | float | Current to be set, in amps. |
| load_impedance | [LoadImpedance](/spikesafe_python_lib_docs/SpikeSafeEnums/README.md) | Selected load impedance compensation. |
| rise_time | [RiseTime](/spikesafe_python_lib_docs/SpikeSafeEnums/README.md) | Selected rise time compensation. |

### Returns
`str`: correction in microseconds with three decimal places and a period decimal
separator. For supported model calculations, negative corrections are limited to
zero and corrections above the firmware limit are capped at
`spikesafe_info.maximum_pulse_width_correction_override`. Unrecognized model
maximum-current values return the default `"1.250"`.

### Raises
`ValueError` if the requested current exceeds `spikesafe_info.maximum_set_current`.

### Example
```python
import spikesafe_python

# tcp_socket is an open SpikeSafe TCP connection.
info = spikesafe_python.SpikeSafeInfoParser.parse_spikesafe_info(tcp_socket)
correction = spikesafe_python.PulseWidthCorrection.get_optimum_pulse_width_correction(
    info, 0.1,
    spikesafe_python.SpikeSafeEnums.LoadImpedance.MEDIUM,
    spikesafe_python.SpikeSafeEnums.RiseTime.MEDIUM,
)
print(correction)
```
