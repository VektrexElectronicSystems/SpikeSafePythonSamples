# Goal: Connect to a SpikeSafe and read all events

import sys
from Utility.SpikeSafeUtility.ReadAllEvents import ReadAllEvents
from Utility.SpikeSafeUtility.TcpSocket import TcpSocket

### set these before starting application

# SpikeSafe IP address
ip_address = '10.0.0.246'

# SpikeSafe port number   
port_number = 8282          

### start of main program
try:
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()

    # connect to SpikeSafe                        
    tcp_socket.openSocket(ip_address, port_number)  
    
    # read all events in SpikeSafe event queue, store in list, and print them to terminal
    event_data = ReadAllEvents(tcp_socket)          
    for event in event_data:                        
        print(event.event)
    
    # disconnect from SpikeSafe
    tcp_socket.closeSocket()                        
except Exception as err:
    # print any error to terminal and exit application
    print('Program error: {}'.format(err))          
    sys.exit(1)

