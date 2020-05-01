# Goal: Connect to a SpikeSafe and run DC Dynamic mode into a shorting plug for 60 seconds
# Expectation: Channel 1 will be driven with 100mA with a forward voltage of ~100mV during this time

import sys
import time
from spikesafe_python.data.MemoryTableReadData import LogMemoryTableRead
from spikesafe_python.utility.spikesafe_utility.ReadAllEvents import LogAllEvents
from spikesafe_python.utility.spikesafe_utility.TcpSocket import TcpSocket
from spikesafe_python.utility.Threading import Wait     

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.246'
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

    # set Channel 1's pulse mode to DC Dynamic and check for all events
    tcp_socket.sendScpiCommand('SOUR1:FUNC:SHAP DCDYNAMIC')    
    LogAllEvents(tcp_socket)

    # set Channel 1's safety threshold for over current protection to 50% and check for all events
    tcp_socket.sendScpiCommand('SOUR1:CURR:PROT 50')    
    LogAllEvents(tcp_socket) 

    # set Channel 1's current to 100 mA and check for all events
    tcp_socket.sendScpiCommand('SOUR1:CURR 0.1')        
    LogAllEvents(tcp_socket)  

    # set Channel 1's voltage to 10 V and check for all events
    tcp_socket.sendScpiCommand('SOUR1:VOLT 10')         
    LogAllEvents(tcp_socket) 

    # turn on Channel 1 and check for all events
    tcp_socket.sendScpiCommand('OUTP1 1')               
    LogAllEvents(tcp_socket)                            

    # check for all events and measure readings on Channel 1 once per second for 60 seconds,
    # it is best practice to do this to ensure Channel 1 is on and does not have any errors
    time_end = time.time() + 60                         
    while time.time() < time_end:                       
        LogAllEvents(tcp_socket)
        LogMemoryTableRead(tcp_socket)
        Wait(1)                            
    
    # turn off Channel 1 and check for all events
    tcp_socket.sendScpiCommand('OUTP1 0')               
    LogAllEvents(tcp_socket)

    # check Channel 1 is off
    LogMemoryTableRead(tcp_socket)

    # disconnect from SpikeSafe                      
    tcp_socket.closeSocket()                            
except Exception as err:
    # print any error to terminal and exit application
    print('Program error: {}'.format(err))          
    sys.exit(1)