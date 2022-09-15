# Examples for Reading All SpikeSafe Events

## Purpose
While operating the SpikeSafe, it is necessary to be aware of any events that may occur that may affect SpikeSafe behavior. The SpikeSafe event queue outputs all events and errors that occur during SpikeSafe operation. The event queue is queried using the SPCI standard `SYST:ERR?` query. The event queue is FIFO, meaning that the first event or error to occur will be the first to be outputted when the queue is queried. Once the SpikeSafe returns `0, OK`, there are no new events or errors.

When the SpikeSafe returns an event, it will be in the format `<code>, <event_message>`. Each specific event message has an associated event code.

Refer to SS400 SCPI Programming Manual Appendix A for a full description of all SpikeSafe events and their expected formats.

## ReadAllEventsManual

### Overview
Demonstrate proper usage of the "Check Event Queue" query on the SpikeSafe. During typical operation, the `SYST:ERR?` query should be sent repeatedly until `0, OK` is received. It is good practice to send this query after any other SCPI command is sent to verify that the SpikeSafe is in the correct state. It is also recommended to send the query periodically while a SpikeSafe channel is running to determine if any events or errors occurs that require action.

### Expected Output
The SpikeSafe will be repeatedly queried until a `0, OK` response is received. The amount of querying will vary based upon the state of the SpikeSafe prior to running this sequence. Sending `MEM:TABL:READ` will have `SYST:ERR?` respond with info event `102, External Paused Signal Stopped` meaning that the SpikeSafe External Pause signal input is not receiving a signal. Sending `SOUR1:VOLT 1` will have `SYST:ERR?` respond with error event `304, Invalid Voltage Setting; SOUR1:VOLT 1` meaning that the SpikeSafe has received an invalid voltage of 1V caused by the the specific SCPI command. 

A typical output is shown below:

`SYST:ERR?`

`102, External Paused Signal Stopped`

`SYST:ERR?`

`0, OK`

`SYST:ERR?`

`304, Invalid Voltage Setting; SOUR1:VOLT 1`

`SYST:ERR?`

`0, OK`

## ReadAllEventsHelper

### Overview
This sample is the same as [ReadAllEventsManual](#readalleventsmanual), except it utilizes [spikesafe-python](https://pypi.org/project/spikesafe-python/) library classes to check the SpikeSafe event queue and raise a SpikeSafe exception on error events. It is encouraged to use [spikesafe-python](https://pypi.org/project/spikesafe-python/) to write simpler and maintainable code, for help on using the library see [spikesafe_python_lib_docs](/spikesafe_python_lib_docs/).

### Expected Output
See [Expected Output](#expected-output)

## Recommended Practices for Reading SpikeSafe Events

### Initial Application Development
Initially it's good practice to call `SYST:ERR?` after every SCPI command to check the SpikeSafe event queue for all events and errors.

#### Examples
[run_spikesafe_operating_modes/run_dc/RunDcMode.py](/run_spikesafe_operating_modes/run_dc/RunDcMode.py)

### Continuous Application Development
Once the application is developed and repeatable, expected behavior is reached, calling `SYST:ERR?` may be optimized to the following scenarios to help an application complete faster by saving roundtrip communication time between the application and SpikeSafe:
1. After all SpikeSafe and PSMU Digitizer settings commands are sent.
2. While a SpikeSafe channel is started.
3. While a PSMU Digitizer is taking measurements.

#### Examples:
[/application_specific_examples/pulse_tuning/PulseTuningExample.py](/application_specific_examples/pulse_tuning/PulseTuningExample.py)  
[/making_integrated_voltage_measurements/measure_voltage_across_pulse/MeasureVoltageAcrossPulse.py](/making_integrated_voltage_measurements/measure_voltage_across_pulse/MeasureVoltageAcrossPulse.py)