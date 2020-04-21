# Goal: Connect to a SpikeSafe and run Bias Pulsed Dynamic mode into a shorting plug for 20 seconds while obtaining readings
#       Settings will be adjusted while running "dynamically" to demonstrate dynamic mode features
# Expectation: Channel 1 will be driven with 100mA with a forward voltage of ~100mV during this time

import sys
import time
from Data.MemoryTableReadData import LogMemoryTableRead
from Utility.SpikeSafeUtility.ReadAllEvents import LogAllEvents
from Utility.SpikeSafeUtility.TcpSocket import TcpSocket
from Utility.Threading import Wait     

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

    # Synchronize rising edge of all channels
    tcp_socket.sendScpiCommand('SOUR1:PULS:STAG 0')   

    # set Channel 1's pulse mode to Pulsed Dynamic and check for all events
    tcp_socket.sendScpiCommand('SOUR1:FUNC:SHAP BIASPULSEDDYNAMIC')

    # set Channel 1's current to 100 mA
    tcp_socket.sendScpiCommand('SOUR1:CURR 0.1')   

    # set Channel 1's voltage to 10 V 
    tcp_socket.sendScpiCommand('SOUR1:VOLT 10') 

    # set Channel 1's bias current to 10 mA and check for all events
    tcp_socket.sendScpiCommand('SOUR1:CURR:BIAS 0.02')   

    # In this example, we specify pulse settings using Pulse Width and Period Commands
    # Unless specifying On Time and Off Time, set pulse HOLD before any other pulse settings
    tcp_socket.sendScpiCommand('SOUR1:PULS:HOLD PERIOD')   

    tcp_socket.sendScpiCommand('SOUR1:PULS:PER 0.01')

    # When Pulse Width is set, Period will not be adjusted at all because we are holding period. Duty Cycle will be adjusted as a result
    tcp_socket.sendScpiCommand('SOUR1:PULS:WIDT 0.001')

    # set Channel 1's compensation settings to their default values
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    tcp_socket.sendScpiCommand('SOUR1:PULS:CCOM 4')
    tcp_socket.sendScpiCommand('SOUR1:PULS:RCOM 4')   

    # Check for any errors with initializing commands
    LogAllEvents(tcp_socket)

    # turn on Channel 1 
    tcp_socket.sendScpiCommand('OUTP1 1')

    # check for all events and measure readings on Channel 1 once per second for 10 seconds,
    # it is best practice to do this to ensure Channel 1 is on and does not have any errors
    time_end = time.time() + 20                         
    while time.time() < time_end:                       
        LogAllEvents(tcp_socket)
        LogMemoryTableRead(tcp_socket)
        Wait(1)

    # turn off Channel 1 after routine is complete
    tcp_socket.sendScpiCommand('OUTP1 0')

    # disconnect from SpikeSafe                      
    tcp_socket.closeSocket()    
except Exception as err:
    # print any error to terminal and exit application
    print('Program error: {}'.format(err))          
    sys.exit(1)


