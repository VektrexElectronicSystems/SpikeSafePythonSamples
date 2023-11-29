# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerData](/spikesafe_python_lib_docs/DigitizerData/README.md) | voltage_reading

## voltage_reading

### Definition
Digitizer voltage reading.

### Attribute Value
[float](https://docs.python.org/3/library/functions.html#float)   

### Examples
The following example demonstrates the voltage_reading attribute. It checks if the PSMU Digitizer has finished measuring voltage data every `wait_time` in milliseconds, fetches its measuremments, and store thems in sample and voltage arrays to be used for plotting in a graph.
```
# wait for the Digitizer measurements to complete 
wait_time = get_new_voltage_data_estimated_complete_time(reading_count, aperture, hardware_trigger_count, hardware_trigger_delay)
wait_for_new_voltage_data(tcp_socket, wait_time)

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