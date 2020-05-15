# Goal: 
# Connect to a SpikeSafe and run Modulated DC mode into an LED, Laser, or electrical component with a custom pulse sequence
#
# Expectation: 
# Channel 1 will be driven with varying current levels up to 150mA, specified within SCPI commands

import sys
import time
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.ReadAllEvents import log_all_events
from spikesafe_python.ReadAllEvents import read_until_event
from spikesafe_python.spikesafe_utility.TcpSocket import TcpSocket
from spikesafe_python.Threading import wait     

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

    # set Channel 1's pulse mode to Modulated DC
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP MODULATED')    

    # set Channel 1's current to 200 mA. This will be the output current when a sequence step specifies "@100"
    tcp_socket.send_scpi_command('SOUR1:CURR 0.2')        

    # set Channel 1's voltage to 20 V
    tcp_socket.send_scpi_command('SOUR1:VOLT 20') 

    # set Channel 1's modulated sequence to a DC staircase with 5 steps
    # There are 5 current steps that each last for 1 second: 40mA, 80mA, 120mA, 160mA, and 200mA
    tcp_socket.send_scpi_command('SOUR1:SEQ 1(1@20,1@40,1@60,1@80,1@100)') 

    # Log all events since all settings are sent
    log_all_events(tcp_socket) 

    # turn on Channel 1
    tcp_socket.send_scpi_command('OUTP1 1')                                         

    # Wait until channel is ready for a trigger command
    read_until_event(tcp_socket, 100) # event 100 is "Channel Ready"

    # Output modulated sequence
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # Wait until channel has completed it modulated sequence
    read_until_event(tcp_socket, 105) # event 105 is "Modulated SEQ completed"

    # turn off Channel 1
    tcp_socket.send_scpi_command('OUTP1 0')      

    # set Channel 1's modulated sequence to an infinite pulsing pattern. This pulsing pattern will repeatedly perform 3 steps:
    #       1.) it will pulse Off for 250ms, then On for 250ms at 120mA. This will happen twice
    #       2.) it will pulse Off for 500ms, then On for 500ms at 60mA. This will also happen twice 
    #       3.) for one second, 180mA will be outputted
    tcp_socket.send_scpi_command('SOUR1:SEQ *(2(.25@0,.25@60),2(.5@0,.5@30),1@90)')          

    # turn on Channel 1
    tcp_socket.send_scpi_command('OUTP1 1')                                         

    # Wait until channel is ready for a trigger command
    read_until_event(tcp_socket, 100) # event 100 is "Channel Ready"

    # Output modulated sequence
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # check for all events and measure readings on Channel 1 once per second for 20 seconds,
    # it is best practice to do this to ensure Channel 1 is on and does not have any errors
    time_end = time.time() + 20                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1)                            
    
    # turn off Channel 1. Since the sequence runs indefinitely, we do not wait for a "Modulated SEQ completed" message
    tcp_socket.send_scpi_command('OUTP1 0')      

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()                            
except Exception as err:
    # print any error to terminal and exit application
    print('Program error: {}'.format(err))          
    sys.exit(1)