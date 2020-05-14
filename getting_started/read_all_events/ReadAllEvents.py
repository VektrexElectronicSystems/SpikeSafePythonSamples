# Goal: 
# Connect to a SpikeSafe and read all events

import sys
from spikesafe_python.ReadAllEvents import read_all_events
from spikesafe_python.TcpSocket import TcpSocket

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282          

### start of main program
try:
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()

    # connect to SpikeSafe                        
    tcp_socket.open_socket(ip_address, port_number)  
    
    # read all events in SpikeSafe event queue, store in list, and print them to terminal
    event_data = read_all_events(tcp_socket)          
    for event in event_data:                        
        print(event.event)
    
    # disconnect from SpikeSafe
    tcp_socket.close_socket()                        
except Exception as err:
    # print any error to terminal and exit application
    print('Program error: {}'.format(err))          
    sys.exit(1)

