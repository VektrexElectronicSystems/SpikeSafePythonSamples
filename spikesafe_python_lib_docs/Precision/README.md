# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Precision](/spikesafe_python_lib_docs/Precision/README.md)

## Precision

### Definition
Provides a collection of helper functions to get the precise number of decimal places for a SpikeSafe SCPI command argument

Formatted numeric arguments always use a period (`.`) as the decimal separator
and no digit grouping, regardless of the application's locale. For example,
`Precision.get_precise_current_command_argument(1.25)` returns `"1.2500"` in both
en-US and de-DE. These functions accept numeric values, rather than localized
strings such as `"1,25"`, and do not change the application's process-wide locale.

### Functions
| Name | Description |
| - | - |
| [Precision.get_precise_compliance_voltage_command_argument(compliance_voltage)](/spikesafe_python_lib_docs/Precision/get_precise_compliance_voltage_command_argument/README.md) | Returns the optimal precision for a compliance voltage command argument. |
| [Precision.get_precise_current_command_argument(current_amps)](/spikesafe_python_lib_docs/Precision/get_precise_current_command_argument/README.md) | Returns the optimal precision for a current in amps command argument. |
| [Precision.get_precise_duty_cycle_command_argument(duty_cycle)](/spikesafe_python_lib_docs/Precision/get_precise_duty_cycle_command_argument/README.md) | Returns the optimal precision for a duty cycle command argument. |
| [Precision.get_precise_pulse_width_correction_command_argument(pulse_width_correction)](/spikesafe_python_lib_docs/Precision/get_precise_pulse_width_correction_command_argument/README.md) | Returns the optimal precision for a pulse width correction command argument. |
| [Precision.get_precise_pulse_width_offset_command_argument(pulse_width_offset)](/spikesafe_python_lib_docs/Precision/get_precise_pulse_width_offset_command_argument/README.md) | Returns the optimal precision for a pulse width offset command argument. |
| [Precision.get_precise_time_command_argument(time_seconds)](/spikesafe_python_lib_docs/Precision/get_precise_time_command_argument/README.md) | Returns the optimal precision for a time in seconds command argument. |
| [Precision.get_precise_time_microseconds_command_argument(time_microseconds)](/spikesafe_python_lib_docs/Precision/get_precise_time_microseconds_command_argument/README.md) | Returns the optimal precision for a time in microseconds command argument. |
| [Precision.get_precise_time_milliseconds_command_argument](/spikesafe_python_lib_docs/Precision/get_precise_time_milliseconds_command_argument/README.md) | Formats a time in milliseconds with three decimal places. |
| [Precision.get_precise_voltage_protection_ramp_dt_command_argument(voltage_protection_ramp_dt)](/spikesafe_python_lib_docs/Precision/get_precise_voltage_protection_ramp_dt_command_argument/README.md) | Returns the optimal precision for a voltage ramp detection dt command argument. |
| [Precision.get_precise_voltage_protection_ramp_dv_command_argument(voltage_protection_ramp_dv)](/spikesafe_python_lib_docs/Precision/get_precise_voltage_protection_ramp_dv_command_argument/README.md) | Returns the optimal precision for a voltage ramp detection dV command argument. |
