# Goal: Connect to a SpikeSafe and run Bias Pulsed mode on all channels into a shorting plug for 20 seconds while obtaining readings
# Expectation: All channels will be driven with 100mA with a forward voltage of ~100mV during this time

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
    tcp_socket.sendScpiCommand('SOUR0:PULS:STAG 0')   

    # set each channel's pulse mode to Pulsed Dynamic
    tcp_socket.sendScpiCommand('SOUR0:FUNC:SHAP BIASPULSED')

    # set each channel's current to 100 mA
    tcp_socket.sendScpiCommand('SOUR0:CURR 0.1')   

    # set each channel's voltage to 10 V 
    tcp_socket.sendScpiCommand('SOUR0:VOLT 10') 

    # set each channel's bias current to 20 mA and check for all events
    tcp_socket.sendScpiCommand('SOUR0:CURR:BIAS 0.02')   

    # In this example, we specify pulse settings using Pulse Width and Period Commands
    # Unless specifying On Time and Off Time, set pulse HOLD before any other pulse settings
    tcp_socket.sendScpiCommand('SOUR0:PULS:HOLD PERIOD')   

    tcp_socket.sendScpiCommand('SOUR0:PULS:PER 0.01')

    # When Pulse Width is set, Period will not be adjusted at all because we are holding period. Duty Cycle will be adjusted as a result
    tcp_socket.sendScpiCommand('SOUR0:PULS:WIDT 0.001')

    # set each channel's compensation settings to their default values
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    tcp_socket.sendScpiCommand('SOUR0:PULS:CCOM 4')
    tcp_socket.sendScpiCommand('SOUR0:PULS:RCOM 4')   

    # Check for any errors with initializing commands
    LogAllEvents(tcp_socket)

    # turn on all channels
    tcp_socket.sendScpiCommand('OUTP0 1')

    # check for all events and measure readings for all channels once per second for 10 seconds,
    # it is best practice to do this to ensure each channel is on and does not have any errors
    time_end = time.time() + 20                         
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


