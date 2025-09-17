# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerDataFetch](/spikesafe_python_lib_docs/DigitizerDataFetch/README.md) | DigitizerDataFetch.get_new_voltage_data_estimated_complete_time(aperture_microseconds, reading_count, hardware_trigger_count=None, hardware_trigger_delay_microseconds=None)

## DigitizerDataFetch.get_new_voltage_data_estimated_complete_time(aperture_microseconds, reading_count, hardware_trigger_count=None, hardware_trigger_delay_microseconds=None)

### Definition
Returns the estimated minimum possible time in seconds it will take for the SpikeSafe PSMU digitizer to acquire new voltage readings. If hardware triggering is used, this does not take into account the pulse period, so the actual time may be longer.

### Parameters
aperture_microseconds [int](https://docs.python.org/3/library/functions.html#int)  
Aperture in microseconds

reading_count [int](https://docs.python.org/3/library/functions.html#int)  
Number of readings to be taken

hardware_trigger_count [int](https://docs.python.org/3/library/functions.html#int) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Number of hardware triggers to be sent. Omit this parameter from the function call when software triggering is used

hardware_trigger_delay_microseconds [int](https://docs.python.org/3/library/functions.html#int) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Delay in microseconds between each hardware trigger. Omit this parameter from the function call when software triggering is used

### Returns
[float](https://docs.python.org/3/library/functions.html#float)  
New voltage data estimated complete time in seconds

### Examples
The following example demonstrates the `get_new_voltage_data_estimated_complete_time()` function. It determines the estimated completion time of the SpikeSafe Digitizer based on the aperture, reading count, hardware trigger delay, and hardware trigger count settings.
```
# set Digitizer aperture for 600µs. Aperture specifies the measurement time, and we want to measure a majority of the pulse's constant current output
aperture = 600
tcp_socket.send_scpi_command(f'VOLT:APER {spikesafe_python.Precision.get_precise_time_microseconds_command_argument(aperture)}')

# set Digitizer trigger delay to 200µs. We want to give sufficient delay to omit any overshoot the current pulse may have
hardware_trigger_delay = 200
tcp_socket.send_scpi_command(f'VOLT:TRIG:DEL {spikesafe_python.Precision.get_precise_time_microseconds_command_argument(hardware_trigger_delay)}')

# set Digitizer trigger source to hardware. When set to a hardware trigger, the digitizer waits for a trigger signal from the SpikeSafe to start a measurement
tcp_socket.send_scpi_command('VOLT:TRIG:SOUR HARDWARE')

# set Digitizer trigger edge to rising. The Digitizer will start a measurement after the SpikeSafe's rising pulse edge occurs
tcp_socket.send_scpi_command('VOLT:TRIG:EDGE RISING')

# set Digitizer trigger count to 525, the maximum value. 525 rising edges of current pulses will correspond to 525 voltage readings
hardware_trigger_count = 525
tcp_socket.send_scpi_command(f'VOLT:TRIG:COUN {hardware_trigger_count}')

# set Digitizer reading count to 1. This is the amount of readings that will be taken when the Digitizer receives its specified trigger signal
reading_count = 1
tcp_socket.send_scpi_command(f'VOLT:READ:COUN {reading_count}')

# check all SpikeSafe event since all settings have been sent
spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

# turn on Channel 1 
tcp_socket.send_scpi_command('OUTP1 1')

# wait until Channel 1 is fully ramped before we take any digitizer measurements. We are looking to measure consistent voltage values
spikesafe_python.ReadAllEvents.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

# start Digitizer measurements
tcp_socket.send_scpi_command('VOLT:INIT')

# wait for the Digitizer measurements to complete. We need to wait for the data acquisition to complete before fetching the data
wait_time = spikesafe_python.DigitizerDataFetch.get_new_voltage_data_estimated_complete_time(reading_count, aperture, hardware_trigger_count, hardware_trigger_delay)
spikesafe_python.DigitizerDataFetch.wait_for_new_voltage_data(tcp_socket, wait_time)

# fetch the Digitizer voltage readings
digitizerData = spikesafe_python.DigitizerDataFetch.fetch_voltage_data(tcp_socket)
```