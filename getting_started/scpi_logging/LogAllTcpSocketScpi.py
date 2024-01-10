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
    log.info("LogAllTcpSocketScpi.py started.")

    log.info("Python version: {}".format(sys.version))
    
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()

    # set TcpSocket to log all SCPI
    tcp_socket.enable_logging = True

    # set TcpSocket to log all SCPI as info level messages
    tcp_socket.default_log_level = 20

    # connect to SpikeSafe
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')

    # request SpikeSafe memory table
    tcp_socket.send_scpi_command('MEM:TABL:READ')

    # read SpikeSafe memory table and print SpikeSafe response to the log file
    data = tcp_socket.read_data()   
    
    # read all events in SpikeSafe event queue, store in list, and print them to the log file
    # here it's expected to receive 1 event: 102, External Pause Signal Ended
    event_data = read_all_events(tcp_socket)
    
    # disconnect from SpikeSafe
    tcp_socket.close_socket()

    log.info("LogAllTcpSocketScpi.py completed.\n")
    
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

