# Goal: Connect to a SpikeSafe and run Modulated DC mode into a shorting plug with a custom pulse sequence
# Expectation: Channel 1 will be driven with varying current levels up to 100mA, specified within SCPI commands

import sys
import time
from spikesafe_python.data.MemoryTableReadData import LogMemoryTableRead
from spikesafe_python.utility.spikesafe_utility.ReadAllEvents import LogAllEvents
from spikesafe_python.utility.spikesafe_utility.ReadAllEvents import read_until_event
from spikesafe_python.utility.spikesafe_utility.TcpSocket import TcpSocket
from spikesafe_python.utility.Threading import wait     

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.241'
port_number = 8282          

### start of main program
try:
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    LogAllEvents(tcp_socket)

    # set Channel 1's pulse mode to Modulated DC
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP MODULATED')    

    # set Channel 1's current to 100 mA
    tcp_socket.send_scpi_command('SOUR1:CURR 0.1')        

    # set Channel 1's voltage to 40 V
    tcp_socket.send_scpi_command('SOUR1:VOLT 40') 

    # set Channel 1's modulated sequence to run 50,000 pulses with 900ms off time and 100ms at the full set current
    tcp_socket.send_scpi_command('SOUR1:SEQ 50000(.9@0,.1@100)') 

    # Log all events since all settings are sent
    LogAllEvents(tcp_socket) 

    # turn on Channel 1
    tcp_socket.send_scpi_command('OUTP1 1')                                         

    # Wait until channel is ready for a trigger command
    read_until_event(tcp_socket, 100) # event 100 is "Channel Ready"

    # Output modulated sequence
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # check for all events and measure readings on Channel 1 once per second for 30 seconds,
    # it is best practice to do this to ensure Channel 1 is on and does not have any errors
    time_end = time.time() + 30                         
    while time.time() < time_end:                       
        LogAllEvents(tcp_socket)
        LogMemoryTableRead(tcp_socket)
        wait(1)                            
    
    # turn off Channel 1
    tcp_socket.send_scpi_command('OUTP1 0')               

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()                            
except Exception as err:
    # print any error to terminal and exit application
    print('Program error: {}'.format(err))          
    sys.exit(1)