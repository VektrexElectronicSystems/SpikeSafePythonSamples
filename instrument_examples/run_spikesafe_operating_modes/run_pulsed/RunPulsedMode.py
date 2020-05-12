
# Goal: Connect to a SpikeSafe and run Pulsed mode into a shorting plug for 15 seconds while obtaining readings
# Expectation: Channel 1 will be driven with 100mA with a forward voltage of ~100mV during this time

import sys
import time
from spikesafe_python.data.MemoryTableReadData import log_memory_table_read
from spikesafe_python.utility.spikesafe_utility.ReadAllEvents import log_all_events
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

    # set Channel 1's pulse mode to Pulsed and check for all events
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP PULSED')
    log_all_events(tcp_socket) 

    # set Channel 1's Pulse On Time to 1ms and check for all events
    tcp_socket.send_scpi_command('SOUR1:PULS:TON 0.001')
    log_all_events(tcp_socket) 

    # set Channel 1's Pulse Off Time to 9ms and check for all events
    tcp_socket.send_scpi_command('SOUR1:PULS:TOFF 0.009')
    log_all_events(tcp_socket) 

    # set Channel 1's safety threshold for over current protection to 50% and check for all events
    tcp_socket.send_scpi_command('SOUR1:CURR:PROT 50')    
    log_all_events(tcp_socket) 

    # set Channel 1's compensation settings to their default values and check for all events
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    tcp_socket.send_scpi_command('SOUR1:PULS:CCOM 4')
    log_all_events(tcp_socket)
    tcp_socket.send_scpi_command('SOUR1:PULS:RCOM 4')   
    log_all_events(tcp_socket)

    # set Channel 1's current to 100 mA and check for all events
    tcp_socket.send_scpi_command('SOUR1:CURR 0.1')   
    log_all_events(tcp_socket)  

    # set Channel 1's voltage to 20 V and check for all events
    tcp_socket.send_scpi_command('SOUR1:VOLT 20')
    log_all_events(tcp_socket)

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # check for all events and measure readings on Channel 1 once per second for 15 seconds,
    # it is best practice to do this to ensure Channel 1 is on and does not have any errors
    time_end = time.time() + 15                        
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1)

    # turn off Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    
except Exception as err:
    # print any error to terminal and exit application
    print('Program error: {}'.format(err))          
    sys.exit(1)


