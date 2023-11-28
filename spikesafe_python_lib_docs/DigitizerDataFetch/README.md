# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerDataFetch](/spikesafe_python_lib_docs/DigitizerDataFetch/README.md)

## DigitizerDataFetch

### Definition
Provides a collection of helper functions you can use to take PSMU Digitizer measurements.

### Functions
| Name | Description |
| - | - |
| [fetch_voltage_data(spike_safe_socket, enable_logging = None)](/spikesafe_python_lib_docs/DigitizerDataFetch/fetch_voltage_data/README.md) | Returns an array of voltage readings from the digitizer obtained through a fetch query. |
| [get_new_voltage_data_estimated_complete_time(aperture_microseconds, reading_count, hardware_trigger_count=None, hardware_trigger_delay_microseconds=None)](/spikesafe_python_lib_docs/DigitizerDataFetch/get_new_voltage_data_estimated_complete_time/README.md) | Returns the estimated time it will take for the SpikeSafe PSMU digitizer to acquire new voltage readings. |
| [wait_for_new_voltage_data(spike_safe_socket, wait_time = 0.0, enable_logging = None)](/spikesafe_python_lib_docs/DigitizerDataFetch/wait_for_new_voltage_data/README.md) | Queries the SpikeSafe PSMU digitizer until it responds that it has acquired new data. |