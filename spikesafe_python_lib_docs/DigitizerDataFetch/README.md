# spikesafe-python API Overview | DigitizerDataFetch

## DigitizerDataFetch

### Definition
Provides a collection of helper functions you can use to take PSMU Digitizer measurements.

### Functions
| Name | Description |
| - | - |
| [fetch_voltage_data(spike_safe_socket)](/spikesafe_python_lib_docs/DigitizerDataFetch/fetch_voltage_data/README.md) | Returns an array of voltage readings from the digitizer obtained through a fetch query. |
| [wait_for_new_voltage_data(spike_safe_socket, wait_time)](/spikesafe_python_lib_docs/DigitizerDataFetch/wait_for_new_voltage_data/README.md) | Queries the SpikeSafe SMU digitizer until it responds that it has acquired new data. |