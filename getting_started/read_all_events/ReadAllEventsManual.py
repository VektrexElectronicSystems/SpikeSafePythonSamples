# Goal: 
# Connect to a SpikeSafe and read all events

import sys
import logging
from spikesafe_python.EventData import EventData
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.SpikeSafeError import SpikeSafeError

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282          

### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(filename='SpikeSafePythonSamples.log',format='%(asctime)s.%(msecs)03d, %(levelname)s, %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)

### start of main program
try:
    log.info("ReadAllEventsManual.py started.")
    
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()

    # connect to SpikeSafe                        
    tcp_socket.open_socket(ip_address, port_number)  

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST') 

    # request SpikeSafe memory table
    tcp_socket.send_scpi_command('MEM:TABL:READ')

    # read SpikeSafe memory table and print SpikeSafe response to the log file
    data = tcp_socket.read_data()   

    # event queue list
    event_queue = []

    # initialize flag to check if event queue is empty 
    is_event_queue_empty = False                                                                                                                      

    # run as long as there is an event in the SpikeSafe queue
    # here it's expected to receive 1 event: 102, External Pause Signal Ended
    while is_event_queue_empty == False:
        # request SpikeSafe events and read data 
        tcp_socket.send_scpi_command('SYST:ERR?')                                        
        event_response = tcp_socket.read_data()

        # event queue is empty
        if event_response.startswith('0'):
            is_event_queue_empty = True
        else:
            # add event to event queue
            event_queue.append(event_response)

    event_data = []

    # convert all events in the SpikeSafe event queue to EventData objects in a new list and print them to the log file
    for event in event_queue:
        event_data_response = EventData().parse_event_data(event)
        event_data.append(event_data_response)
        log.info(event_data_response.event)
        log.info(event_data_response.code)
        log.info(event_data_response.message)
        log.info(','.join(map(str, event_data_response.channel_list)))

    # set Channel 1's voltage to an invalid 1 V and check for all events
    tcp_socket.send_scpi_command('SOUR1:VOLT 1')

    # clear event queue list
    event_queue.clear()

    # initialize flag to check if event queue is empty 
    is_event_queue_empty = False                                                                                                                      

    # run as long as there is an event in the SpikeSafe queue
    # here it's expected to receive 1 event: 304, Invalid Voltage Setting; SOUR1:VOLT 1
    while is_event_queue_empty == False:
        # request SpikeSafe events and read data 
        tcp_socket.send_scpi_command('SYST:ERR?')                                        
        event_response = tcp_socket.read_data()

        # event queue is empty
        if event_response.startswith('0'):
            is_event_queue_empty = True
        else:
            # add event to event queue
            event_queue.append(event_response)
    
    # convert all events in the SpikeSafe event queue to EventData objects in a new list
    for event in event_queue:
        event_data_response = EventData().parse_event_data(event)

        # raise a SpikeSafeError for any event codes 200 and greater that correspond to SpikeSafe Errors. In general, operation should stop for these
        # here it's expected to raise a SpikeSafeError for event: 304, Invalid Voltage Setting; SOUR1:VOLT 1
        if (event_data_response.code > 200):
            raise SpikeSafeError(event_data_response.code, event_data_response.message, event_data_response.channel_list, event_data_response.event)
    
    # disconnect from SpikeSafe
    tcp_socket.close_socket()

    log.info("ReadAllEventsManual.py completed.\n")
    
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

