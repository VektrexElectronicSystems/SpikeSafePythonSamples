# Goal: 
# Connect to a SpikeSafe and read all events

import sys
import logging
from spikesafe_python.ReadAllEvents import read_all_events
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.SpikeSafeError import SpikeSafeError

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282          

### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(filename='SpikeSafePythonSamples.log',format='%(asctime)s, %(levelname)s, %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)

### start of main program
try:
    log.info("ReadAllEvents.py started.")
    
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()

    # connect to SpikeSafe                        
    tcp_socket.open_socket(ip_address, port_number)  
    
    # read all events in SpikeSafe event queue, store in list, and print them to the log file
    event_data = read_all_events(tcp_socket)          
    for event in event_data:                        
        log.info(event.event)
        log.info(event.code)
        log.info(event.message)
        log.info(','.join(map(str, event.channel_list)))
    
    # disconnect from SpikeSafe
    tcp_socket.close_socket()   

    log.info("ReadAllEvents.py completed.\n")
    
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

