# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerData](/spikesafe_python_lib_docs/DigitizerData/README.md) | voltage_reading_volts_formatted_float(self)

## voltage_reading_volts_formatted_float(self)

### Definition
Returns the voltage reading rounded to seven decimal places as a float.

### Returns
[float](https://docs.python.org/3/library/functions.html#float)  
Returns the voltage reading rounded to seven decimal places as a float.

### Examples
The following example demonstrates the voltage_reading attribute. It checks if the PSMU Digitizer has finished measuring voltage data every 500 milliseconds, fetches its measuremments, and store thems in sample and voltage arrays to be used for plotting in a graph.
```
# wait for the Digitizer measurements to complete 
spikesafe_python.DigitizerDataFetch.wait_for_new_voltage_data(tcp_socket, 0.5)

# fetch the Digitizer voltage readings using VOLT:FETC? query
digitizerData = []
digitizerData = spikesafe_python.DigitizerDataFetch.fetch_voltage_data(tcp_socket)

# prepare digitizer voltage data to plot
samples = []
voltage_readings = []
for dd in digitizerData:
    samples.append(dd.sample_number)
    voltage_readings.append(dd.voltage_reading_volts_formatted_float())
```

### Examples In Action
