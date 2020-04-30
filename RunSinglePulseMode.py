# Goal: Connect to a SpikeSafe and run Single Pulse mode on all channels into a shorting plug and output to all channels
# Expectation: All channels will output a 100mA pulse with a pulse width of 1ms. This will happen 3 times. Expecting a low (<1V) forward voltage

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

    # set each channel's pulse mode to Single Pulse
    tcp_socket.sendScpiCommand('SOUR0:FUNC:SHAP SINGLEPULSE')

    # set each channel's current to 100 mA
    tcp_socket.sendScpiCommand('SOUR0:CURR 0.1')     

    # set each channel's voltage to 10 V 
    tcp_socket.sendScpiCommand('SOUR0:VOLT 10')   

    # set each channel's pulse width to 1ms. Of the pulse time settings, only Pulse On Time and Pulse Width [+Offset] are relevant in Single Pulse mode
    tcp_socket.sendScpiCommand('SOUR0:PULS:WIDT 0.001')

    # set each channel's compensation settings to their default values
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    tcp_socket.sendScpiCommand('SOUR0:PULS:CCOM 4')
    tcp_socket.sendScpiCommand('SOUR0:PULS:RCOM 4')   

    # Check for any errors with initializing commands
    LogAllEvents(tcp_socket)

    # turn on all channels
    tcp_socket.sendScpiCommand('OUTP0 1')

    # Wait until channels are ready for a trigger command
    ReadUntilEvent(tcp_socket, 100) # event 100 is "Channel Ready"

    # Output 1ms pulse for all channels
    tcp_socket.sendScpiCommand('OUTP0:TRIG')

    # check for all events and measure readings on each channel once per second for 2 seconds,
    # it is best practice to do this to ensure each channel is on and does not have any errors
    time_end = time.time() + 2                         
    while time.time() < time_end:                       
        LogAllEvents(tcp_socket)
        LogMemoryTableRead(tcp_socket)
        Wait(1)        

    # Output 1ms pulse for all channels. Multiple pulses can be outputted while the channel is enabled
    tcp_socket.sendScpiCommand('OUTP0:TRIG')

    # check for all events and measure readings after the second pulse output
    time_end = time.time() + 2                         
    while time.time() < time_end:                       
        LogAllEvents(tcp_socket)
        LogMemoryTableRead(tcp_socket)
        Wait(1) 

    # Output 1ms pulse for all channels
    tcp_socket.sendScpiCommand('OUTP0:TRIG')

    # check for all events and measure readings after the last pulse output
    time_end = time.time() + 2                         
    while time.time() < time_end:                       
        LogAllEvents(tcp_socket)
        LogMemoryTableRead(tcp_socket)
        Wait(1) 

    # turn off all channels after routine is complete
    tcp_socket.sendScpiCommand('OUTP0 0')

    # disconnect from SpikeSafe                      
    tcp_socket.closeSocket()    
except Exception as err:
    # print any error to terminal and exit application
    print('Program error: {}'.format(err))          
    sys.exit(1)