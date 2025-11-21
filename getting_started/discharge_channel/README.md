# Examples for Discharging a SpikeSafe PRF or PSMU Channel

## **Purpose**
Demonstrate how to use a SpikeSafe PRF or PSMU to deliver high precision DC current to an LED or Laser load to increase its forward voltage for testing, once testing is complete turn off the current supply, and then wait to properly discharge the load voltage before taking any further action such as delivering current again to the load or removing it.

Newer SpikeSafe Firmware versions support using the SpikeSafe Get Discharge Complete query, while older firmware versions rely manually waiting on a time delay to properly discharge the load. This sample demonstrates how to determine which implementation to use.

## **Discharge SpikeSafe Channel Using Get Discharge Complete query**

### Overview 
Operates the first test using SpikeSafe as a DC current source with single output current, stops current output, and then polls the SpikeSafe Get Discharge Complete query to properly discharge the load with the intent of running a second test. Afterwards, the same process is repeated for the second and final test with the intent of ensuring the load is safe to be disconnected. 

In this process, [`spikesafe_python.SpikeSafeInfoParser.parse_spikesafe_info()`](../../spikesafe_python_lib_docs/SpikeSafeInfoParser/parse_spikesafe_info/README.md) is used to retrieve [`spikesafe_python.SpikeSafeInfo.supports_discharge_query`](../../spikesafe_python_lib_docs/SpikeSafeInfo/supports_discharge_query/README.md), which determined to use [`spikesafe_python.Discharge.wait_for_spikesafe_channel_discharge()`](../../spikesafe_python_lib_docs/Discharge/wait_for_spikesafe_channel_discharge/README.md).

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
Operates SpikeSafe as a DC current source with single output current, stops current output, and then waits to properly discharge the load with the intent of running a second test. Afterwards, the same process is repeated for the second and final test with the intent of ensuring the load is safe to be disconnected.

In this process, [`spikesafe_python.SpikeSafeInfoParser.parse_spikesafe_info()`](../../spikesafe_python_lib_docs/SpikeSafeInfoParser/parse_spikesafe_info/) is used to retrieve [`spikesafe_python.SpikeSafeInfo.supports_discharge_query`](../../spikesafe_python_lib_docs/SpikeSafeInfo/supports_discharge_query/), which determined to use [`spikesafe_python.Discharge.get_spikesafe_channel_discharge_time()`](../../spikesafe_python_lib_docs/Discharge/get_spikesafe_channel_discharge_time/) and [`spikesafe_python.Threading.wait()`](../../spikesafe_python_lib_docs/Threading/wait/).

### Expected Output
Once the delay to discharge after the first test has completed, the second test begins supplying output current again to the load. Once the second test has completed, another delay to discharge occurs until all load voltage is discharged to notify the operator that it is safe to be disconnected.

Each delay will show the following message in the log:   
Waiting 0.027 seconds for Channel 1 to fully discharge...

### Remarks
System timers dictate the resolution of time delays. See [Remarks](../../spikesafe_python_lib_docs/Threading/wait/README.md#remarks) describing resolution of system timers between operating systems.