# spikesafe-python API Overview | DigitizerDataFetch | wait_for_new_voltage_data(spike_safe_socket, wait_time)

## wait_for_new_voltage_data(spike_safe_socket, wait_time)

### Definition
Queries the SpikeSafe SMU digitizer until it responds that it has acquired new data.

### Parameters
spike_safe_socket [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md)  
Socket object used to communicate with SpikeSafe.

wait_time [float](https://docs.python.org/3/library/functions.html#float)
Wait time in between each set of queries, in seconds (0 by default).   

### Examples
The following example demonstrates the wait_for_new_voltage_data function. It checks if the PSMU Digitizer has finished measuring voltage data every 500 milliseconds, fetches its measuremments, and store thems in sample and voltage arrays to be used for plotting in a graph.
```
# wait for the Digitizer measurements to complete 
wait_for_new_voltage_data(tcp_socket, 0.5)

# fetch the Digitizer voltage readings using VOLT:FETC? query
digitizerData = []
digitizerData = fetch_voltage_data(tcp_socket)

# prepare digitizer voltage data to plot
samples = []
voltage_readings = []
for dd in digitizerData:
    samples.append(dd.sample_number)
    voltage_readings.append(dd.voltage_reading)
```

### Examples In Action
[/making_integrated_voltage_measurements/measure_voltage_across_pulse/MeasureVoltageAcrossPulse.py](/making_integrated_voltage_measurements/measure_voltage_across_pulse/MeasureVoltageAcrossPulse.py)