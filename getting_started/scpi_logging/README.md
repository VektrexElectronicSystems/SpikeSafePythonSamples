# Examples for SCPI Logging

## Purpose
While operating the SpikeSafe, it might be necessary to be aware of the SCPI communication transmitting back and forth between the SpikeSafe and the computer via TCP/IP socket. Logging SCPI communication to a file may be used to help correct initial setup issues in order to produce a repeatable test setup.

All SCPI messages will log to SpikeSafePythonSamples.log under the root directory of the SpikeSafePythonSamples repository (...\SpikeSafePythonSamples\).

All SCPI messages will log in the following format:
`<datetime>, <log level>, <message (if logging SCPI, will prepend with: TcpSocket <IP address>)>`

## LogAllTcpSocketScpi

### Overview
Logging SCPI communication may be turned on at a TCP/IP socket level.

### Expected Output
Logging all SCPI on a TCP/IP socket will automatically capture connection attempts, disconnection attempts, sending SCPI, and reading SCPI.

A typical output in SpikeSafePythonSamples.log is shown below:

09/13/2022 04:57:26, INFO, LogAllTcpSocketScpi.py started.  
09/13/2022 04:57:29, INFO, TcpSocket 10.0.0.220. Connecting...  
09/13/2022 04:57:29, INFO, TcpSocket 10.0.0.220. Sending SCPI command: *RST  
09/13/2022 04:57:29, INFO, TcpSocket 10.0.0.220. Sending SCPI command: MEM:TABL:READ  
09/13/2022 04:57:29, INFO, TcpSocket 10.0.0.220. Read Data reply: (DIF (NAME "Output Readings" (DATA (BULK 99.7) (CH1 0.000000 0.000000 0) (T1 29.9) (T2 29.9) (T3 0.0) (T4 0.0) )))  
09/13/2022 04:57:29, INFO, TcpSocket 10.0.0.220. Sending SCPI command: SYST:ERR?  
09/13/2022 04:57:29, INFO, TcpSocket 10.0.0.220. Read Data reply: 102, External Paused Signal Stopped  
09/13/2022 04:57:29, INFO, TcpSocket 10.0.0.220. Sending SCPI command: SYST:ERR?  
09/13/2022 04:57:29, INFO, TcpSocket 10.0.0.220. Read Data reply: 0, OK  
09/13/2022 04:57:29, INFO, TcpSocket 10.0.0.220. Disconnecting...  
09/13/2022 04:57:29, INFO, LogAllTcpSocketScpi.py completed.  

## LogSpecificTcpSocketScpi

### Overview
Logging SCPI communication may be turned for specific TCP/IP socket activity.

### Expected Output
Logging specific SCPI communication will capture sending SCPI and reading SCPI only upon request.

A typical output in SpikeSafePythonSamples.log is shown below:

09/13/2022 04:57:35, INFO, LogSpecificTcpSocketScpi.py started.  
09/13/2022 04:57:36, INFO, TcpSocket 10.0.0.231. Read Data reply: (DIF (NAME "Output Readings" (DATA (BULK 99.8) (CH1 0.000000 0.000000 0) (T1 29.9) (T2 29.9) (T3 0.0) (T4 0.0) )))  
09/13/2022 04:57:36, INFO, TcpSocket 10.0.0.231. Sending SCPI command: SYST:ERR?  
09/13/2022 04:57:36, INFO, TcpSocket 10.0.0.231. Read Data reply: 102, External Paused Signal Stopped  
09/13/2022 04:57:36, INFO, TcpSocket 10.0.0.231. Sending SCPI command: SYST:ERR?  
09/13/2022 04:57:36, INFO, TcpSocket 10.0.0.231. Read Data reply: 0, OK  
09/13/2022 04:57:36, INFO, LogSpecificTcpSocketScpi.py completed.  