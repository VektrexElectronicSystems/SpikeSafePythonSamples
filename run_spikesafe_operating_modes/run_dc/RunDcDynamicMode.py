# Goal: 
# Connect to a SpikeSafe and run DC Dynamic mode into an LED, Laser, or electrical component
# Demonstrate the concept of changing current Set Point dynamically (while the channel is outputting)
#
# Expectation: 
# Channel 1 will initially be driven with 50mA with a forward voltage of < 1V during this time. While running change the current to 100mA, 150mA, 200mA, then 100mA again

import sys
import time
import logging
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.ReadAllEvents import log_all_events
from spikesafe_python.ReadAllEvents import read_until_event
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.Threading import wait     

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282          

### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(filename='SpikeSafePythonSamples.log',format='%(asctime)s, %(levelname)s, %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)

### start of main program
try:
    log.info("RunDcDynamicMode.py started.")
    
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # set Channel 1's pulse mode to DC Dynamic and check for all events
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP DCDYNAMIC')    
    log_all_events(tcp_socket)

    # set Channel 1's safety threshold for over current protection to 50% and check for all events
    tcp_socket.send_scpi_command('SOUR1:CURR:PROT 50')    
    log_all_events(tcp_socket) 

    # set Channel 1's current to 50 mA and check for all events
    tcp_socket.send_scpi_command('SOUR1:CURR 0.05')        
    log_all_events(tcp_socket)  

    # set Channel 1's voltage to 10 V and check for all events
    tcp_socket.send_scpi_command('SOUR1:VOLT 20')         
    log_all_events(tcp_socket) 

    # turn on Channel 1 and check for all events
    tcp_socket.send_scpi_command('OUTP1 1')               
    log_all_events(tcp_socket)                            

    # wait until the channel is fully ramped
    read_until_event(tcp_socket, 100) # event 100 is "Channel Ready"

    # check for all events and measure readings on Channel 1 once per second for 10 seconds,
    # it is best practice to do this to ensure Channel 1 is on and does not have any errors
    time_end = time.time() + 10                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1)    

    # While the channel is running, dynamically change the Set Current to 100mA. Check events and measure readings afterward
    tcp_socket.send_scpi_command('SOUR1:CURR 0.1')        
    log_all_events(tcp_socket)
    log_memory_table_read(tcp_socket)
    wait(1)

    # While the channel is running, dynamically change the Set Current to 150mA. Check events and measure readings afterward
    tcp_socket.send_scpi_command('SOUR1:CURR 0.15')        
    log_all_events(tcp_socket)
    log_memory_table_read(tcp_socket)
    wait(1)

    # While the channel is running, dynamically change the Set Current to 200mA. Check events and measure readings afterward
    tcp_socket.send_scpi_command('SOUR1:CURR 0.2')        
    log_all_events(tcp_socket)
    log_memory_table_read(tcp_socket)
    wait(1)

    # While the channel is running, dynamically change the Set Current to 100mA. Check events and measure readings afterward
    tcp_socket.send_scpi_command('SOUR1:CURR 0.1')        
    log_all_events(tcp_socket)
    log_memory_table_read(tcp_socket)
    wait(1)
    
    # turn off Channel 1 and check for all events
    tcp_socket.send_scpi_command('OUTP1 0')               
    log_all_events(tcp_socket)

    # check Channel 1 is off
    log_memory_table_read(tcp_socket)

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()     

    log.info("RunDcDynamicMode.py completed.\n")

except Exception as err:
    # print any error to the log file and exit application
    log.error('Program error: {}'.format(err))          
    sys.exit(1)