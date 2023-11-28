# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerDataFetch](/spikesafe_python_lib_docs/DigitizerDataFetch/README.md) | get_new_voltage_data_estimated_complete_time(aperture_microseconds, reading_count, hardware_trigger_count=None, hardware_trigger_delay_microseconds=None)

## get_new_voltage_data_estimated_complete_time(aperture_microseconds, reading_count, hardware_trigger_count=None, hardware_trigger_delay_microseconds=None)

### Definition
Returns the estimated time it will take for the SpikeSafe PSMU digitizer to acquire new voltage readings.

### Parameters
aperture_microseconds [int](https://docs.python.org/3/library/functions.html#int)  
Aperture in microseconds

reading_count [int](https://docs.python.org/3/library/functions.html#int)  
Number of readings to be taken

hardware_trigger_count [int](https://docs.python.org/3/library/functions.html#int) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Number of hardware triggers to be sent

hardware_trigger_delay_microseconds [int](https://docs.python.org/3/library/functions.html#int) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Delay in microseconds between each hardware trigger

### Returns
[float](https://docs.python.org/3/library/functions.html#float)  
New voltage data estimated complete time in seconds