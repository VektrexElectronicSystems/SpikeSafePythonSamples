# Examples for Discharging a SpikeSafe PRF or PSMU Channel

## **Purpose**
Demonstrate how to use a SpikeSafe PRF or PSMU to deliver high precision DC current to an LED or Laser load to increase its forward voltage for testing, once testing is complete turn off the current supply, and then wait to properly discharge the load voltage before taking any further action such as delivering current again to the load or removing it.

Vektrex recommends using the SpikeSafe Get Discharge Complete query to properly discharge the load voltage. This is available starting with SpikeSafe Firmware Version 3.6.1 consisting of Rev 3.0.5.5 and DSP version 2.0.45. Refer to [Discharge SpikeSafe Channel Using Get Discharge Complete query](#discharge-spikesafe-channel-using-get-discharge-complete-query) below.

For older SpikeSafe Firmware Versions, use a time delay to properly discharge the load voltage. Refer to [Discharge SpikeSafe Channel Using Time Delay](#discharge-spikesafe-channel-using-time-delay) below.

## **Discharge SpikeSafe Channel Using Get Discharge Complete query**

### Overview 
Operates the first test using SpikeSafe as a DC current source with single output current, stops current output, and then uses the SpikeSafe Get Discharge Complete query to properly discharge the load with the intent of running a second test. Afterwards, the same process is repeated for the second and final test, then the SpikeSafe Discharge Complete query is used again with the intent of ensuring the load is safe to be disconnected.

### Expected Output
Once the SpikeSafe Get Discharge Complete query returns `TRUE` after the first test has completed, the second test begins supplying output current again to the load. Once the second test has completed, the SpikeSafe Get Discharge Complete query is monitored until all load voltage is discharged to notify the operator that it is safe be disconnected.

#### Log Output Between test #1 and test #2
Sending SCPI command: `OUTP1 0`  
`0, OK`  
Waiting for Channel 1 to fully discharge after test #1...  
Sending SCPI command: `OUTP1:DISC:COMP?`  
Read Data reply: `FALSE`  
Sending SCPI command: `OUTP1:DISC:COMP?`  
Read Data reply: `FALSE`  
Sending SCPI command: `OUTP1:DISC:COMP?`  
Read Data reply: `FALSE`  
Sending SCPI command: `OUTP1:DISC:COMP?`  
Read Data reply: `FALSE`  
Sending SCPI command: `OUTP1:DISC:COMP?`  
Read Data reply: `FALSE`  
Sending SCPI command: `OUTP1:DISC:COMP?`  
Read Data reply: `TRUE`  
Sending SCPI command: `OUTP1 1`

#### Log Output Between test #2 and Completing the Script
Sending SCPI command: `OUTP1 0`  
`0, OK`  
Waiting for Channel 1 to fully discharge after test #2...  
Sending SCPI command: `OUTP1:DISC:COMP?`  
Read Data reply: `FALSE`  
Sending SCPI command: `OUTP1:DISC:COMP?`  
Read Data reply: `FALSE`  
Sending SCPI command: `OUTP1:DISC:COMP?`  
Read Data reply: `FALSE`  
Sending SCPI command: `OUTP1:DISC:COMP?`  
Read Data reply: `FALSE`  
Sending SCPI command: `OUTP1:DISC:COMP?`  
Read Data reply: `FALSE`  
Sending SCPI command: `OUTP1:DISC:COMP?`  
Read Data reply: `FALSE`  
Sending SCPI command: `OUTP1:DISC:COMP?`  
Read Data reply: `TRUE`  
discharge_channel_using_delay.py completed.

## **Discharge SpikeSafe Channel Using Time Delay**

### Overview
Operates SpikeSafe as a DC current source with single output current, stops current output, and then uses the [spikesafe-python](https://pypi.org/project/spikesafe-python/) [`spikesafe_python.Discharge.get_spikesafe_channel_discharge_time()`](../../spikesafe_python_lib_docs/Discharge/spikesafe_python.Discharge.get_spikesafe_channel_discharge_time/) and [`spikesafe_python.Threading.wait()`](../../spikesafe_python_lib_docs/Threading/wait/) functions to properly discharge the load with the intent of running a second test. Afterwards, the same process is repeated for the second and final test, then the SpikeSafe Discharge Complete query is used again with the intent of ensuring that it is safe to be disconnected.

### Expected Output
Once the delay to discharge after the first test has completed, the second test begins supplying output current again to the load. Once the second test has completed, another delay to discharge occurs until all load voltage is discharged to notify the operator that it is safe to be disconnected.

Each delay will show the following message in the log:   
Waiting 0.027 seconds for Channel 1 to fully discharge...

### Remarks
System timers dictate the resolution of time delays. See [Remarks](../../spikesafe_python_lib_docs/Threading/wait/README.md#remarks) describing resolution of system timers between operating systems.