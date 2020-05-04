# Goal: Connect to a SpikeSafe and run Multi Pulse mode on Channel 1 into a shorting plug
# Expectation: All channels will output a 100mA pulse with a pulse width of 1ms and a Bias Current of 10mA. This will happen 3 times. 
#               Expecting a low (<1V) forward voltage

import sys
import time
from spikesafe_python.data.MemoryTableReadData import log_memory_table_read
from spikesafe_python.utility.spikesafe_utility.ReadAllEvents import log_all_events
from spikesafe_python.utility.spikesafe_utility.ReadAllEvents import read_until_event
from spikesafe_python.utility.spikesafe_utility.TcpSocket import TcpSocket
from spikesafe_python.utility.Threading import wait     

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282          

### start of main program
try:
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # set Channel 1's pulse mode to Multi Pulse
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP MULTIPULSE')

    # set Channel 1's current to 100 mA
    tcp_socket.send_scpi_command('SOUR1:CURR 0.1') 

    # set Channel 1's voltage to 10 V 
    tcp_socket.send_scpi_command('SOUR1:VOLT 10')   

    # set Channel 1's Pulse On Time and Pulse Off Time to 1s each
    tcp_socket.send_scpi_command('SOUR1:PULS:TON 1')
    tcp_socket.send_scpi_command('SOUR1:PULS:TOFF 1')

    # set Channel 1's Pulse Count to 3. Every trigger will output 3 pulses
    tcp_socket.send_scpi_command('SOUR1:PULS:COUN 3')

    # set Channel 1's compensation settings to their default values
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    tcp_socket.send_scpi_command('SOUR1:PULS:CCOM 4')
    tcp_socket.send_scpi_command('SOUR1:PULS:RCOM 4')   

    # Check for any errors with initializing commands
    log_all_events(tcp_socket)

    # turn on Channel 1
    tcp_socket.send_scpi_command('OUTP1 1')

    # Wait until channel is ready for a trigger command
    read_until_event(tcp_socket, 100) # event 100 is "Channel Ready"

    # Output 1ms pulse for Channel 1
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # check for all events and measure readings on the channel once per second for 2 seconds,
    # it is best practice to do this to ensure the channel is on and does not have any errors
    time_end = time.time() + 2                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1)        

    # check that the Multi Pulse output has ended
    hasMultiPulseEndedString = ''
    while hasMultiPulseEndedString != b'TRUE\n':
        tcp_socket.send_scpi_command('SOUR1:PULS:END?')
        hasMultiPulseEndedString =  tcp_socket.read_data()
        wait(0.5)

    # Output 1ms pulse for Channel 1. Multiple pulses can be outputted while the channel is enabled
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # check for all events and measure readings after the second pulse output
    time_end = time.time() + 2                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1) 

    # check that the Multi Pulse output has ended
    hasMultiPulseEndedString = ''
    while hasMultiPulseEndedString != b'TRUE\n':
        tcp_socket.send_scpi_command('SOUR1:PULS:END?')
        hasMultiPulseEndedString =  tcp_socket.read_data()
        wait(0.5)

    # turn off all Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    
except Exception as err:
    # print any error to terminal and exit application
    print('Program error: {}'.format(err))          
    sys.exit(1)