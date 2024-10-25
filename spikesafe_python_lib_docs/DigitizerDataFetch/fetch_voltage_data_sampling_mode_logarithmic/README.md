# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerDataFetch](/spikesafe_python_lib_docs/DigitizerDataFetch/README.md) | fetch_voltage_data_sampling_mode_logarithmic(spike_safe_socket, time_sampling_mode, sampling_mode, hardware_trigger_delay_microseconds = 0, enable_logging = None)

## fetch_voltage_data_sampling_mode_logarithmic(spike_safe_socket, time_sampling_mode, sampling_mode, hardware_trigger_delay_microseconds = 0, enable_logging = None)

### Definition
Returns an array of voltage readings using logarithmic sampling mode from the digitizer obtained through a fetch query.

### Parameters
spike_safe_socket [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md)  
Socket object used to communicate with SpikeSafe.

time_sampling_mode : [TimeSamplingMode](/spikesafe_python_lib_docs/DigitizerEnums/TimeSamplingMode/README.md)  
The time sampling mode to use for the voltage data. This should be an instance of the TimeSamplingMode enum from DigitizerEnums.

sampling_mode : [SamplingMode](/spikesafe_python_lib_docs/DigitizerEnums/SamplingMode/README.md)  
The sampling mode to use for the voltage data. This should be an instance of the SamplingMode enum from DigitizerEnums.

hardware_trigger_delay_microseconds : [int](https://docs.python.org/3/library/functions.html#int) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
The hardware trigger delay in microseconds (default to 0us)

enable_logging : [bool](https://docs.python.org/3/library/stdtypes.html#boolean-values) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Overrides spike_safe_socket.enable_logging attribute (None by default, will use spike_safe_socket.enable_logging value).

### Returns
[DigitizerData array](/spikesafe_python_lib_docs/DigitizerData/README.md)  
Contains an array of DigitizerData objects which have a defined voltage_reading, sample_number, and time_since_start_seconds attribute.

### Examples
The following example demonstrates the fetch_voltage_data function. It checks if the PSMU Digitizer has finished measuring voltage data every 500 milliseconds, fetches its measuremments, and store thems in sample and voltage arrays to be used for plotting in a graph.
```
# wait for the Digitizer measurements to complete 
wait_for_new_voltage_data(tcp_socket, 0.5)

# fetch the Digitizer voltage readings using VOLT:FETC? query
digitizerData = []
digitizerData = fetch_voltage_data_sampling_mode_logarithmic(
        spike_safe_socket=tcp_socket,
        time_sampling_mode=TimeSamplingMode.MIDDLE_OF_TIME,
        sampling_mode=SamplingMode.FAST_LOG
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