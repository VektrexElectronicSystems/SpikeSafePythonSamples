# Goal: Connect to a SpikeSafe and run Pulsed Sweep mode on Channel 1 into a shorting plug and run two complete Pulsed Sweeps
# Expectation: Channel 1 will run a sweep from 20mA to 200mA, which will take 100ms. Expecting a low (<1V) forward voltage

import sys
import time
from spikesafe_python.data.MemoryTableReadData import LogMemoryTableRead
from spikesafe_python.utility.spikesafe_utility.ReadAllEvents import LogAllEvents
from spikesafe_python.utility.spikesafe_utility.ReadAllEvents import ReadUntilEvent
from spikesafe_python.utility.spikesafe_utility.TcpSocket import TcpSocket
from spikesafe_python.utility.Threading import Wait     

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282          

### start of main program
try:
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.openSocket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.sendScpiCommand('*RST')                  
    LogAllEvents(tcp_socket)

    # set Channel 1's pulse mode to Pulsed Sweep and check for all events
    tcp_socket.sendScpiCommand('SOUR1:FUNC:SHAP PULSEDSWEEP')

    # set Channel 1's Pulsed Sweep parameter to match the test expectation
    tcp_socket.sendScpiCommand('SOUR1:CURR:STAR 0.02')
    tcp_socket.sendScpiCommand('SOUR1:CURR:STOP 0.2')   
    tcp_socket.sendScpiCommand('SOUR1:CURR:STEP 100')   

    # set Channel 1's voltage to 10 V 
    tcp_socket.sendScpiCommand('SOUR1:VOLT 10')   

    # set Channel 1's pulse settings for a 1% duty cycle and 1ms Period using the Pulse On Time and Pulse Off Time commands
    tcp_socket.sendScpiCommand('SOUR1:PULS:TON 0.0001')
    tcp_socket.sendScpiCommand('SOUR1:PULS:TOFF 0.0099')

    # set Channel 1's compensation settings to their default values
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    tcp_socket.sendScpiCommand('SOUR1:PULS:CCOM 4')
    tcp_socket.sendScpiCommand('SOUR1:PULS:RCOM 4')   

    # Check for any errors with initializing commands
    LogAllEvents(tcp_socket)

    # turn on Channel 1 
    tcp_socket.sendScpiCommand('OUTP1 1')

    # Wait until Channel 1 is ready for a trigger command
    ReadUntilEvent(tcp_socket, 100) # event 100 is "Channel Ready"

    # Output pulsed sweep for Channel 1
    tcp_socket.sendScpiCommand('OUTP1:TRIG')

    # Wait for the Pulsed Sweep to be complete
    ReadUntilEvent(tcp_socket, 109) # event 109 is "Pulsed Sweep Complete"

    # Output pulsed sweep for Channel 1. Multiple sweeps can be run while the channel is enabled
    tcp_socket.sendScpiCommand('OUTP1:TRIG')

    # Wait for the Pulsed Sweep to be complete
    ReadUntilEvent(tcp_socket, 109) # event 109 is "Pulsed Sweep Complete"

    # turn off Channel 1 after routine is complete
    tcp_socket.sendScpiCommand('OUTP1 0')

    # disconnect from SpikeSafe                      
    tcp_socket.closeSocket()    
except Exception as err:
    # print any error to terminal and exit application
    print('Program error: {}'.format(err))          
    sys.exit(1)