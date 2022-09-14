# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerDataFetch](/spikesafe_python_lib_docs/DigitizerDataFetch/README.md)

## DigitizerDataFetch

### Definition
Provides a collection of helper functions you can use to take PSMU Digitizer measurements.

### Functions
| Name | Description |
| - | - |
| [fetch_voltage_data(spike_safe_socket, enable_logging = None)](/spikesafe_python_lib_docs/DigitizerDataFetch/fetch_voltage_data/README.md) | Returns an array of voltage readings from the digitizer obtained through a fetch query. |
| [wait_for_new_voltage_data(spike_safe_socket, wait_time = 0.0, enable_logging = None)](/spikesafe_python_lib_docs/DigitizerDataFetch/wait_for_new_voltage_data/README.md) | Queries the SpikeSafe SMU digitizer until it responds that it has acquired new data. |