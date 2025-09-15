# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerData](/spikesafe_python_lib_docs/DigitizerData/README.md) | time_since_start_seconds

## time_since_start_seconds

### Definition
Time since the start of the sampling in seconds.

### Attribute Value
[float](https://docs.python.org/3/library/functions.html#float)   

### Examples
The following example demonstrates the voltage_reading attribute. It checks if the PSMU Digitizer has finished measuring voltage data every 500 milliseconds, fetches its measuremments, and store thems in sample and voltage arrays to be used for plotting in a graph.
```
# wait for the Digitizer measurements to complete 
spikesafe_python.wait_for_new_voltage_data(tcp_socket, 0.5)

# fetch the Digitizer voltage readings using VOLT:FETC? query
digitizerData = []
digitizerData = spikesafe_python.fetch_voltage_data_sampling_mode_linear(
        spike_safe_socket=tcp_socket,
        time_sampling_mode=spikesafe_python.DigitizerEnums.TimeSamplingMode.MIDDLE_OF_TIME,
        aperture_microseconds=2,
        reading_count=3,
        hardware_trigger_delay_microseconds=0,
        pulse_period_seconds=0
    )

# prepare digitizer voltage data to plot
samples = []
voltage_readings = []
time_since_start_seconds = []
for dd in digitizerData:
    samples.append(dd.sample_number)
    time_since_start_seconds.append(dd.time_since_start_seconds)
    voltage_readings.append(dd.voltage_reading)
```

### Examples In Action
[/making_integrated_voltage_measurements/measure_voltage_across_pulse/MeasureVoltageAcrossPulse.py](/making_integrated_voltage_measurements/measure_voltage_across_pulse/MeasureVoltageAcrossPulse.py)