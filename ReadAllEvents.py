# Goal: Connect to a SpikeSafe and read all events

import sys
from Utility.SpikeSafeUtility.ReadAllEvents import ReadAllEvents
from Utility.SpikeSafeUtility.TcpSocket import TcpSocket

# set these before starting application
ip_address = '10.0.0.246'   # SpikeSafe IP address
port_number = 8282          # SpikeSafe port number

# start of main program
try:
    tcp_socket = TcpSocket()                        # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket.openSocket(ip_address, port_number)  # connect to SpikeSafe
    event_data = ReadAllEvents(tcp_socket)          # read all events in SpikeSafe event queue and store in list
    for event in event_data:                        # print all SpikeSafe events to terminal
        print(event.event)
    tcp_socket.closeSocket()                        # disconnect from SpikeSafe
except Exception as err:
    print('Program error: {}'.format(err))          # print any error to terminal
    sys.exit(1)                                     # exit application on any error

