# spikesafe-python API Overview | DigitizerData | sample_number

## sample_number

### Definition
Sample number of the voltage reading

### Attribute Value
[int](https://docs.python.org/3/library/functions.html#int)  

### Examples
The following example demonstrates the sample_number attribute. It instructs the PSMU Digitizer to take voltage measurement samples and store them in sample and voltage arrays to be used for plotting in a graph.
```
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