# Goal: Connect to a SpikeSafe and run Bias Pulsed Dynamic mode into a shorting plug for 20 seconds while obtaining readings
#       Settings will be adjusted while running "dynamically" to demonstrate dynamic mode features
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

    # Synchronize rising edge of all channels
    tcp_socket.send_scpi_command('SOUR1:PULS:STAG 0')   

    # set Channel 1's pulse mode to Pulsed Dynamic and check for all events
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP BIASPULSEDDYNAMIC')

    # set Channel 1's current to 100 mA
    tcp_socket.send_scpi_command('SOUR1:CURR 0.1')   

    # set Channel 1's voltage to 10 V 
    tcp_socket.send_scpi_command('SOUR1:VOLT 10') 

    # set Channel 1's bias current to 20 mA and check for all events
    tcp_socket.send_scpi_command('SOUR1:CURR:BIAS 0.02')   

    # In this example, we specify pulse settings using Pulse Width and Period Commands
    # Unless specifying On Time and Off Time, set pulse HOLD before any other pulse settings
    tcp_socket.send_scpi_command('SOUR1:PULS:HOLD PERIOD')   

    tcp_socket.send_scpi_command('SOUR1:PULS:PER 0.01')

    # When Pulse Width is set, Period will not be adjusted at all because we are holding period. Duty Cycle will be adjusted as a result
    tcp_socket.send_scpi_command('SOUR1:PULS:WIDT 0.001')

    # set Channel 1's compensation settings to their default values
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    tcp_socket.send_scpi_command('SOUR1:PULS:CCOM 4')
    tcp_socket.send_scpi_command('SOUR1:PULS:RCOM 4')   

    # Check for any errors with initializing commands
    log_all_events(tcp_socket)

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # check for all events and measure readings on Channel 1 once per second for 10 seconds,
    # it is best practice to do this to ensure Channel 1 is on and does not have any errors
    time_end = time.time() + 10                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1)

    # set Channel 1's current to 150 mA while running
    tcp_socket.send_scpi_command('SOUR1:CURR 0.15')      

    # set Channel 1's Pulse Width to 2 ms while running. The Duty Cycle will be adjusted as a result
    tcp_socket.send_scpi_command('SOUR1:PULS:WIDT 0.002')

    # Run for 10 more seconds while checking all events and measuring readings for Channel 1
    time_end = time.time() + 10                         
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


