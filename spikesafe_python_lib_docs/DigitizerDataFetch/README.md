# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerDataFetch](/spikesafe_python_lib_docs/DigitizerDataFetch/README.md)

## DigitizerDataFetch

### Definition
Provides a collection of helper functions you can use to take PSMU Digitizer measurements.

### Functions
| Name | Description |
| - | - |
| [fetch_voltage_data(spike_safe_socket, enable_logging = None)](/spikesafe_python_lib_docs/DigitizerDataFetch/fetch_voltage_data/README.md) | Returns an array of voltage readings from the digitizer obtained through a fetch query. |
| [fetch_voltage_data_sampling_mode_custom(spike_safe_socket, time_sampling_mode, custom_sequence, hardware_trigger_delay_microseconds = 0, enable_logging = None)](/spikesafe_python_lib_docs/DigitizerDataFetch/fetch_voltage_data_sampling_mode_custom/README.md) | Returns an array of voltage readings using custom sampling mode from the digitizer obtained through a fetch query. |
| [fetch_voltage_data_sampling_mode_linear(spike_safe_socket, time_sampling_mode, aperture_microseconds, reading_count, hardware_trigger_delay_microseconds = 0, pulse_period_seconds = 0, enable_logging = None)](/spikesafe_python_lib_docs/DigitizerDataFetch/fetch_voltage_data_sampling_mode_linear/README.md) | Returns an array of voltage readings using linear sampling mode from the digitizer obtained through a fetch query. |
| [fetch_voltage_data_sampling_mode_logarithmic(spike_safe_socket, time_sampling_mode, sampling_mode, hardware_trigger_delay_microseconds = 0, enable_logging = None)](/spikesafe_python_lib_docs/DigitizerDataFetch/fetch_voltage_data_sampling_mode_logarithmic/README.md) | Returns an array of voltage readings using logarithmic sampling mode from the digitizer obtained through a fetch query. |
| [get_new_voltage_data_estimated_complete_time(aperture_microseconds, reading_count, hardware_trigger_count=None, hardware_trigger_delay_microseconds=None)](/spikesafe_python_lib_docs/DigitizerDataFetch/get_new_voltage_data_estimated_complete_time/README.md) | Returns the estimated minimum possible time it will take for the SpikeSafe PSMU digitizer to acquire new voltage readings. If hardware triggering is used, this does not take into account the pulse period, so the actual time may be longer. |
| [wait_for_new_voltage_data(spike_safe_socket, wait_time = 0.0, enable_logging = None)](/spikesafe_python_lib_docs/DigitizerDataFetch/wait_for_new_voltage_data/README.md) | Queries the SpikeSafe PSMU digitizer until it responds that it has acquired new data. |