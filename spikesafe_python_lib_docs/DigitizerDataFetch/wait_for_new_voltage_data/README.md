# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerDataFetch](/spikesafe_python_lib_docs/DigitizerDataFetch/README.md) | spikesafe_python.wait_for_new_voltage_data(spike_safe_socket, wait_time = 0.0, enable_logging = None)

## spikesafe_python.wait_for_new_voltage_data(spike_safe_socket, wait_time = 0.0, enable_logging = None, timeout = None)

### Definition
Queries the SpikeSafe PSMU digitizer until it responds that it has acquired new data.

### Parameters
spike_safe_socket [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md)  
Socket object used to communicate with SpikeSafe.

wait_time [float](https://docs.python.org/3/library/functions.html#float) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Wait time in between each set of queries, in seconds (0 by default).

enable_logging [bool](https://docs.python.org/3/library/stdtypes.html#boolean-values) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Overrides spike_safe_socket.enable_logging attribute (None by default, will use spike_safe_socket.enable_logging value).

timeout [float](https://docs.python.org/3/library/functions.html#float) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Timeout in seconds for waiting for new data. If None, wait indefinitely.

### Examples
The following example demonstrates the spikesafe_python.wait_for_new_voltage_data function. It checks if the PSMU Digitizer has finished measuring voltage data every 500 milliseconds, fetches its measuremments, and store thems in sample and voltage arrays to be used for plotting in a graph.
```
# wait for the Digitizer measurements to complete 
spikesafe_python.wait_for_new_voltage_data(tcp_socket, 0.5)

# fetch the Digitizer voltage readings using VOLT:FETC? query
digitizerData = []
digitizerData = spikesafe_python.fetch_voltage_data(tcp_socket)

# prepare digitizer voltage data to plot
samples = []
voltage_readings = []
for dd in digitizerData:
    samples.append(dd.sample_number)
    voltage_readings.append(dd.voltage_reading)
```

### Examples In Action
[/making_integrated_voltage_measurements/measure_voltage_across_pulse/MeasureVoltageAcrossPulse.py](/making_integrated_voltage_measurements/measure_voltage_across_pulse/MeasureVoltageAcrossPulse.py)