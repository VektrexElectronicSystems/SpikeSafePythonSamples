# Goal: 
# Connect to a SpikeSafe and run Bias mode into an LED, Laser, or electrical component

# Expectation: 
# Channel 1 will be driven with 10mA with a forward voltage of <1V during this time
# Sequence will wait for the channel to be fully stable, and then power the DUT for 10 seconds

import sys
import time
import logging
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.ReadAllEvents import log_all_events
from spikesafe_python.ReadAllEvents import read_until_event
from spikesafe_python.SpikeSafeEvents import SpikeSafeEvents
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.Threading import wait  
from spikesafe_python.SpikeSafeError import SpikeSafeError   

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282

### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d, %(levelname)s, %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S',
    handlers=[
        logging.FileHandler("SpikeSafePythonSamples.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

### start of main program
try:
    log.info("RunBiasMode.py started.")

    log.info("Python version: {}".format(sys.version))
    
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # set Channel 1's pulse mode to DC and check for all events
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP BIAS')    
    log_all_events(tcp_socket)

    # set Channel 1's safety threshold for over current protection to 50% and check for all events
    tcp_socket.send_scpi_command('SOUR1:CURR:PROT 50')    
    log_all_events(tcp_socket) 

    # set Channel 1's bias current to 10 mA and check for all events
    tcp_socket.send_scpi_command('SOUR1:CURR:BIAS 0.01')        
    log_all_events(tcp_socket)  

    # set Channel 1's voltage to 10 V and check for all events
    tcp_socket.send_scpi_command('SOUR1:VOLT 10')         
    log_all_events(tcp_socket) 

    # turn on Channel 1 and check for all events
    tcp_socket.send_scpi_command('OUTP1 1')               
    log_all_events(tcp_socket)                            

    # wait until the channel is fully ramped to 10mA
    read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # check for all events and measure readings on Channel 1 once per second for 15 seconds,
    # it is best practice to do this to ensure Channel 1 is on and does not have any errors
    time_end = time.time() + 10                         
    while time.time() < time_end:                       
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

    log.info("RunBiasMode.py completed.\n")

except SpikeSafeError as ssErr:
    # print any SpikeSafe-specific error to both the terminal and the log file, then exit the application
    error_message = 'SpikeSafe error: {}\n'.format(ssErr)
    log.error(error_message)
    print(error_message)
    sys.exit(1)
except Exception as err:
    # print any general exception to both the terminal and the log file, then exit the application
    error_message = 'Program error: {}\n'.format(err)
    log.error(error_message)       
    print(error_message)   
    sys.exit(1)