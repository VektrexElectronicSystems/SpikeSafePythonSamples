# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerDataFetch](/spikesafe_python_lib_docs/DigitizerDataFetch/README.md) | fetch_voltage_data_sampling_mode_custom(spike_safe_socket, time_sampling_mode, custom_sequence, hardware_trigger_delay_microseconds = 0, enable_logging = None)

## fetch_voltage_data_sampling_mode_custom(spike_safe_socket, time_sampling_mode, custom_sequence, hardware_trigger_delay_microseconds = 0, enable_logging = None)

### Definition
Returns an array of voltage readings using custom sampling mode from the digitizer obtained through a fetch query.

### Parameters
spike_safe_socket [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md)  
Socket object used to communicate with SpikeSafe.

time_sampling_mode : [TimeSamplingMode](/spikesafe_python_lib_docs/DigitizerEnums/TimeSamplingMode/README.md)  
The time sampling mode to use for the voltage data. This should be an instance of the TimeSamplingMode enum from DigitizerEnums.

custom_sequence : [string](https://docs.python.org/3/library/string.html) 
The custom sequence to use for the voltage data

hardware_trigger_delay_microseconds : [int](https://docs.python.org/3/library/functions.html#int) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
The hardware trigger delay in microseconds (default to 0us)

enable_logging : [bool](https://docs.python.org/3/library/stdtypes.html#boolean-values) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Overrides spike_safe_socket.enable_logging attribute (None by default, will use spike_safe_socket.enable_logging value).

### Returns
[DigitizerData array](/spikesafe_python_lib_docs/DigitizerData/README.md)  
Contains an array of DigitizerData objects which have a defined voltage_reading, sample_number, and time_since_start_seconds attribute.

### Examples
The following example demonstrates the spikesafe_python.fetch_voltage_data function. It checks if the PSMU Digitizer has finished measuring voltage data every 500 milliseconds, fetches its measuremments, and store thems in sample and voltage arrays to be used for plotting in a graph.
```
# wait for the Digitizer measurements to complete 
spikesafe_python.DigitizerDataFetch.wait_for_new_voltage_data(tcp_socket, 0.5)

# fetch the Digitizer voltage readings using VOLT:FETC? query
digitizerData = []
digitizer_data = spikesafe_python.DigitizerDataFetch.fetch_voltage_data_sampling_mode_custom(
        spike_safe_socket=tcp_socket,
        time_sampling_mode=spikesafe_python.DigitizerEnums.TimeSamplingMode.MIDDLE_OF_TIME,
        custom_sequence="50@2,2@4,7@6,6@8,4@10,4@12,3@14,2@16,3@18,2@20,2@22,2@24,1@26,2@28,1@30,2@32,1@34,1@36,1@38,1@40,2@42,1@46,1@48,1@50,1@52,1@54,1@56,1@60,1@62,1@66,1@68,1@72,1@74,1@78,1@82,1@86,1@90,1@94,1@98,1@104,1@108,1@114,1@118,1@124,1@130,1@136,1@142,1@150,1@156,1@164,1@172,1@180,1@188,1@196,1@206,1@216,1@226,1@236,1@248,1@258,1@272,1@284,1@298,1@312,1@326,1@342,1@358,1@374,1@392,1@410,1@430,1@450"
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